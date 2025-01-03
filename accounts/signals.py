from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from allauth.socialaccount.models import SocialToken

# Print out the access_token and id_token for 'api/auth/{provider}/' endpoint
@receiver(social_account_added)
def fetch_tokens_after_social_account_added(request, sociallogin, **kwargs):
    social_account = sociallogin.account
    print(social_account)
    if social_account:
        tokens = SocialToken.objects.filter(account=social_account)
        if tokens.exists():
            access_token = tokens.first().token
            print(f"Access Token: {access_token}")

            if social_account.provider == 'google':
                id_token = tokens.first().token_secret
                print(f"ID Token: {id_token}")
        else:
            print("No tokens found for this social account.")
