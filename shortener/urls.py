from django.urls import path
from .api_views import URLListAPIView
from . import views

urlpatterns = [
    path('api/urls/', URLListAPIView.as_view(), name='api_urls'),       # Retrieve short URLs created by the user with JWT (For front-end and back-end separation framework)
    path('list/', views.url_list, name='url_list'),                     # Retrieve short URLs created by the user
    path('list/create/', views.url_create, name='url_create'),          # Create short URL
    path('<str:short_url>/', views.url_redirect, name='url_redirect'),  # Redirect using short URL
]
