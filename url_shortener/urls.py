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
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from rest_framework.response import Response


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user

        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
        except SocialAccount.DoesNotExist:
            return Response({'error': 'SocialAccount not found'}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

urlpatterns = [
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'), # Login with access_token, key, id_token to get the token for the endpoint "'api/urls/'"
    path('api/auth/facebook/', FacebookLogin.as_view(), name='facebook_login'), # Similiar to the process of google
    path('data_deletion_policy/', data_deletion_policy, name='data_deletion'), #For app publication review of Facebook
    path('privacy_policy/', privacy_policy, name='privacy'), #For app publication review of Facebook
    path('admin/', admin.site.urls), # Default admin page
    path('accounts/3rdparty/', custom_connections_view, name='account_connections'), # Override default allauth 3rdparty
    path('accounts/logout/', auto_logout, name='account_logout'), # Logout Router
    path('accounts/', include('allauth.urls')),  # Login Router
    path('', include('shortener.urls')),   # Shortener App
    path('', lambda request: redirect('url_list')), # Set url_list as the home page
]
