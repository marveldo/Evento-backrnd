"""
ASGI config for evento project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evento.settings")
django.setup()

from ws.auth import CustomTokenAuthMiddleware 
from channels.routing import ProtocolTypeRouter,URLRouter
from ws.middleware import CorsHostValidator
from ws.routing import ws_url_patterns
from users.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    "websocket" : CorsHostValidator(
        CustomTokenAuthMiddleware(
            URLRouter(
              ws_url_patterns + websocket_urlpatterns
            )
        )
    )
})

