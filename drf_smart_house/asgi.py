import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import home.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_smart_house.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        home.routing.websocket_urlpatterns
    ),
})
