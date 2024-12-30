from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from allauth.socialaccount.views import ConnectionsView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.http import require_GET

@require_GET
@login_required
def auto_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

@require_GET
@login_required
def custom_connections_view(request, *args, **kwargs):
    if not request.user.is_superuser:  # Only for Admin
        return HttpResponseForbidden("Access denied")
    return ConnectionsView.as_view()(request, *args, **kwargs)