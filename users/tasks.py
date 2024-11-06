from background_task import background
from datetime import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import User
# from .serializers import Userserializer
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken

def send_welcome_email(user):

    """Function to send email to user upon registeration
    """
    subject = 'Welcome To evento'
    email_from = settings.EMAIL_HOST_USER
    email_to = user.email

    context ={
        'user' : user,
        'url' : f'{settings.FRONTEND_LINK}/login'
    }

    html_message = render_to_string('welcome.html', context)
    message = strip_tags(html_message)
    send_mail(
        subject=subject,
        message=message,
       from_email=email_from,
       recipient_list=[email_to],
       html_message=html_message
       )

def get_user_from_access_token(access_token):
    """Function that handles getting a User from access_token

    Args:
        access_token (str): access token generated during login

    Returns:
        dict: returns the users details
    """
    access = AccessToken(access_token)
    user  = User.objects.get(id = access.payload.get('user_id'))
    serializer = {
        'id' : str(user.id),
        'full_name': user.full_name,
        'email': user.email
    }
    return serializer


@background
def run_send_mail(user_id):
    try  :
        user = User.objects.get(id=str(user_id))
        send_welcome_email(user=user)
    except User.DoesNotExist :
        print('failed')
    
    
   
    

