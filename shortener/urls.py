from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.url_list, name='url_list'),                     # Retrieve short URLs created by the user
    path('list/create/', views.url_create, name='url_create'),          # Create short URL
    path('<str:short_url>/', views.url_redirect, name='url_redirect'),  # Redirect using short URL
]
