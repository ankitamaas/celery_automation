"""
ASGI config for my_keyword_scraper project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_keyword_scraper.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django_asgi_app = get_asgi_application()

import scraper.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket":AuthMiddlewareStack(URLRouter(scraper.routing.websocket_urlpatterns))
    }
)