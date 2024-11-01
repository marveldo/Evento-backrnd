from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import AnonymousUser
from users.models import User
from urllib.parse import parse_qs
import logging




@database_sync_to_async
def get_user(access_token : str) -> User :

    """Function to retrieve the user from access_token

    Args:
        access_token (str): access token passed in

    Returns:
        User: Returns the user model
    """
    try:
        user_id = AccessToken(access_token).payload.get('user_id')
        user = User.objects.get(id = user_id)
        return user
    except (User.DoesNotExist, TokenError)  : 
        return AnonymousUser()
    

class CustomTokenAuthMiddleware(BaseMiddleware):
    """Class For Custom Authentication Middle ware

    Args:
        BaseMiddleware (_type_): _description_
    """

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        """Check if an accesstoken is in the query param and returns the User that owns the access token

        Args:
            scope (_type_): contains information about the incoming websocket request
            receive (_type_): event listner for when a message is received
            send (_type_): event listener when a message is sent
        """
        query_string = scope['query_string'].decode('utf-8')
        query_params = dict(parse_qs(query_string))
        access_token = query_params.get('access_token',[None])[0]
        if access_token is None :
            scope['user'] = AnonymousUser()
        else :
            scope['user'] = await get_user(access_token)
        return await super().__call__(scope, receive, send)
    
    









    

