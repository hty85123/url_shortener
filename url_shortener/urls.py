"""
URL configuration for url_shortener project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from accounts.views import custom_connections_view, auto_logout
from shortener.views import data_deletion_policy, privacy_policy

urlpatterns = [
    path('data_deletion_policy/', data_deletion_policy, name='data_deletion'),
    path('privacy_policy/', privacy_policy, name='privacy'),
    path('admin/', admin.site.urls),
    path('accounts/3rdparty/', custom_connections_view, name='account_connections'),
    path('accounts/logout/', auto_logout, name='account_logout'),
    path('accounts/', include('allauth.urls')),  # Login Router
    path('', include('shortener.urls')),   # Shortener App
    path('', lambda request: redirect('url_list')),
    
]
