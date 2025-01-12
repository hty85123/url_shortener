from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShortenedURL, ClickRecord
import time
import requests
from django.db import connection, transaction
from collections import namedtuple
from datetime import datetime

URLData = namedtuple('URLData', ['original_url', 'short_url', 'clicks_count', 'clicks'])

# # With N+1 Problem
# # Retrieve short URLs created by the user
# @login_required
# def url_list(request):
#     with connection.cursor() as cursor:
#         # Retrieve urls related to the user
#         cursor.execute("""
#             SELECT id, original_url, short_url
#             FROM shortener_shortenedurl
#             WHERE user_id = %s
#         """, [request.user.id])
#         urls = cursor.fetchall()

#     url_data = []
#     for url in urls:
#         url_id, original_url, short_url = url

#         with connection.cursor() as cursor:
#             # Count of Clicks
#             cursor.execute("""
#                 SELECT COUNT(*) FROM shortener_clickrecord
#                 WHERE short_url_id = %s
#             """, [url_id])
#             clicks_count = cursor.fetchone()[0]

#             # Click Records
#             cursor.execute("""
#                 SELECT timestamp, ip_address
#                 FROM shortener_clickrecord
#                 WHERE short_url_id = %s
#                 ORDER BY timestamp DESC
#             """, [url_id])
#             clicks = cursor.fetchall()
#         url_data.append(URLData(
#             original_url=original_url,
#             short_url=short_url,
#             clicks_count=clicks_count,
#             clicks=[{'timestamp': c[0], 'ip_address': c[1]} for c in clicks],
#         ))
#     return render(request, 'shortener/url_list.html', {'urls': url_data})

# Retrieve short URLs created by the user
@login_required
def url_list(request):
    with connection.cursor() as cursor:
        # Retrieve short url and click records
        cursor.execute("""
            SELECT 
                su.id AS url_id, 
                su.original_url, 
                su.short_url, 
                COUNT(cr.id) AS clicks_count
            FROM shortener_shortenedurl su
            LEFT JOIN shortener_clickrecord cr ON su.id = cr.short_url_id
            WHERE su.user_id = %s
            GROUP BY su.id, su.original_url, su.short_url
        """, [request.user.id])
        urls = cursor.fetchall()
    # Retreive click records 
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                cr.short_url_id, 
                cr.timestamp, 
                cr.ip_address
            FROM shortener_clickrecord cr
            INNER JOIN shortener_shortenedurl su ON cr.short_url_id = su.id
            WHERE su.user_id = %s
            ORDER BY cr.short_url_id, cr.timestamp DESC
        """, [request.user.id])
        all_clicks = cursor.fetchall()
    # Store retreived click records using Dict
    clicks_dict = {}
    for short_url_id, timestamp, ip_address in all_clicks:
        if short_url_id not in clicks_dict:
            clicks_dict[short_url_id] = []
        clicks_dict[short_url_id].append({'timestamp': timestamp, 'ip_address': ip_address})

    # output data
    url_data = []
    for url_id, original_url, short_url, clicks_count in urls:
        url_data.append(URLData(
            original_url=original_url,
            short_url=short_url,
            clicks_count=clicks_count,
            clicks=clicks_dict.get(url_id, [])
        ))

    return render(request, 'shortener/url_list.html', {'urls': url_data})


# Create short URL
@login_required
def url_create(request):
    if request.method == 'POST':
        original_url = request.POST['original_url']
        is_valid, warning_message = is_valid_url(original_url)
        if not is_valid:
            messages.error(request, warning_message)
            return render(request, 'shortener/url_create.html')
        try:
            with transaction.atomic():  # Start a transaction block
                with connection.cursor() as cursor:
                    # Check if URL already exists
                    cursor.execute("""
                        SELECT id, short_url
                        FROM shortener_shortenedurl
                        WHERE original_url = %s AND user_id = %s
                    """, [original_url, request.user.id])
                    existing_url = cursor.fetchone()

                    if existing_url:
                        return redirect('url_list')
                    # Insert new URL record
                    cursor.execute("""
                        INSERT INTO shortener_shortenedurl (original_url, short_url ,user_id, created_at)
                        VALUES (%s, %s, %s, %s)
                    """, [original_url, "", request.user.id, datetime.now()])
                    # Retrieve last inserted ID
                    new_url_id = cursor.lastrowid
                    # Generate and update short URL
                    short_url = generate_short_url(new_url_id, request.user.id)
                    cursor.execute("""
                        UPDATE shortener_shortenedurl
                        SET short_url = %s
                        WHERE id = %s
                    """, [short_url, new_url_id])
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'shortener/url_create.html')

        return redirect('url_list')

    return render(request, 'shortener/url_create.html')

def is_valid_url(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        # Connect successfully
        if response.status_code >= 400:
            # Non 2xx series status code. Notify user but still shorten the URL.
            return True, f"Warning: URL returned status code {response.status_code}."
        return True, None
    except requests.exceptions.RequestException:
        return False, "Error: URL connection failed. Please check if it is valid."


# Base62 Encoding
def base62_encode(num):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = 62
    encoded = []
    while num > 0:
        remainder = num % base
        encoded.append(characters[remainder])
        num //= base
    return ''.join(reversed(encoded))

# Generate snowflake-liked ID and encode it using Base62
def generate_short_url(record_id, user_id):
    timestamp = int(time.time())
    composite_id = int(f"{record_id}{timestamp}{user_id}")
    return base62_encode(composite_id)


# Redirect using short URL
def url_redirect(request, short_url):
    url = get_object_or_404(ShortenedURL, short_url=short_url)
    ip_address = get_client_ip(request)
    ClickRecord.objects.create(short_url=url, ip_address=ip_address)
    return redirect(url.original_url)

#Recored IP related to the click about the short URL
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def data_deletion_policy(request):
    return render(request, 'shortener/data_deletion_policy.html')

def privacy_policy(request):
    return render(request, 'shortener/privacy_policy.html')