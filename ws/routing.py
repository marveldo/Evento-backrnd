from django.urls import re_path
from .consumer import BaseWebsocketConsumer
ws_url_patterns = [
    re_path(r"^ws/home/$", BaseWebsocketConsumer.as_asgi())
]