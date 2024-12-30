from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShortenedURL, ClickRecord
import time
import requests


# Retrieve short URLs created by the user
@login_required
def url_list(request):
    urls = ShortenedURL.objects.filter(user=request.user)
    return render(request, 'shortener/url_list.html', {'urls': urls})


# Create short URL
@login_required
def url_create(request):
    if request.method == 'POST':
        original_url = request.POST['original_url']
        is_valid, warning_message = is_valid_url(original_url)
        if not is_valid:
            messages.error(request, warning_message)
            return render(request, 'shortener/url_create.html')

        if warning_message:
            # Short URL that has the response with non-2xx series status code
            messages.warning(request, warning_message)

        existing_url = ShortenedURL.objects.filter(original_url=original_url, user=request.user).first()
        if existing_url:
            return redirect('url_list')

        new_url = ShortenedURL.objects.create(
            original_url=original_url,
            user=request.user
        )

        new_url.short_url = generate_short_url(new_url.id, request.user.id)
        new_url.save()

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
