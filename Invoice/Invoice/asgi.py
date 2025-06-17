import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Invoice.settings')

# Initialize Django ASGI application early
django_asgi_app = get_asgi_application()

# Import routing after Django is initialized
from Invoice_admin.routing import websocket_urlpatterns
from .token_auth import TokenAuthMiddleware  # We'll create this

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(  # Our custom middleware
            AuthMiddlewareStack(  # Django's session auth
                URLRouter(websocket_urlpatterns)
            )
        )
    ),
})