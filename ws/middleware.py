from channels.security.websocket import OriginValidator
from django.conf import settings


def CorsHostValidator(application):
    allowed_hosts = settings.ALLOWED_HOSTS
    if settings.DEBUG and not allowed_hosts:
        allowed_hosts = ["localhost", "127.0.0.1", "[::1]"]
    cors_allowed_origins = settings.CORS_ALLOWED_ORIGINS + allowed_hosts
    return OriginValidator(application=application , allowed_origins=cors_allowed_origins)

