# config/asgi.py

import os

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.asgi import get_asgi_application

# Standard Django ASGI application
django_asgi_app = get_asgi_application()

# Channels routing
from channels.routing import ProtocolTypeRouter, URLRouter
from community.middleware import TokenAuthMiddleware
import community.routing

application = ProtocolTypeRouter(
    {
        # HTTP → Django
        "http": django_asgi_app,

        # WebSocket → Channels
        "websocket": TokenAuthMiddleware(
            URLRouter(community.routing.websocket_urlpatterns)
        ),
    }
)


