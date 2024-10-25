from google.auth.transport import requests
from google.oauth2 import id_token
from .models import User
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from .tasks import run_send_mail




class Google():
    """Class For google auth
    """

    @staticmethod
    def validate(access_token : str):
        """Function to validate access_token

        Args:
            access_token (str): access token to be validated
        """
        
        try :
           id_info = id_token.verify_oauth2_token(access_token, requests.Request(), clock_skew_in_seconds=10)
           if "accounts.google.com" in id_info['iss']:
               return id_info
        except Exception as e :
           return "Token is invalid or has expired"
def register_social_auth_user(provider, email,full_name,picture):
    """_summary_

    Args:
        provider (_type_): _description_
        email (_type_): _description_
        full_name (_type_): _description_
    """
    users = User.objects.filter(email=email)
    if users.exists():
        access_token = AccessToken.for_user(users[0])
        refresh_token = RefreshToken.for_user(users[0])
        return {
            "status_code": 200,
            "access": str(access_token),
            "refresh": str(refresh_token)
        }
    user = User.objects.create(
        full_name = full_name,
        email = email,
        auth_provider = provider,
        profile_img = picture
    )
    user.set_password(settings.SOCIAL_AUTH_PASSWORD)
    user.is_verified = True
    user.save()
    run_send_mail(user_id=str(user.id))
    access_token = AccessToken.for_user(user)
    refresh_token = RefreshToken.for_user(user)
    return {
        "status_code":201,
        "access": str(access_token),
        "refresh": str(refresh_token)
    }