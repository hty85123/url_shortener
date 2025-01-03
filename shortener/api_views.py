from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from collections import namedtuple

URLData = namedtuple('URLData', ['original_url', 'short_url', 'clicks_count'])

class URLListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, original_url, short_url
                FROM shortener_shortenedurl
                WHERE user_id = %s
            """, [request.user.id])
            urls = cursor.fetchall()

        url_data = []
        for url in urls:
            url_id, original_url, short_url = url
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) FROM shortener_clickrecord
                    WHERE short_url_id = %s
                """, [url_id])
                clicks_count = cursor.fetchone()[0]
            url_data.append(URLData(original_url, short_url, clicks_count))

        return Response({'urls': [u._asdict() for u in url_data]})

