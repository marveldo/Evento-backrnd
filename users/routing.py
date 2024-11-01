from .consumers import NotificationsConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'^ws/notifications/$', NotificationsConsumer.as_asgi())
]
