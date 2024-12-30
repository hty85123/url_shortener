from django.conf import settings

def custom_settings(request):
    return {
        'LOGIN_BY_CODE_ENABLED': getattr(settings, 'LOGIN_BY_CODE_ENABLED', False),
        'PASSKEY_LOGIN_ENABLED': getattr(settings, 'PASSKEY_LOGIN_ENABLED', False),
    }

def base_url(request):
    return {
        'BASE_URL': settings.BASE_URL
    }