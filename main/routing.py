from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from users.consumers import LoginConsumer
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        URLRouter([
            path('ws/login/', LoginConsumer.as_asgi())
        ])
    )
})
