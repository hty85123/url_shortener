from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return
        try:
            user = User.objects.get(email=email)
            sociallogin.connect(request, user)
        except ObjectDoesNotExist:
            pass


    def is_open_for_signup(self, request, sociallogin, **kwargs):
        return True
