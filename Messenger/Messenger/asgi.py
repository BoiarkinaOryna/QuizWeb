"""
ASGI config for Mesenger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack # клас, що авторизує користувачів
from django.core.asgi import get_asgi_application
from chats.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Messenger.settings')

application = ProtocolTypeRouter({
    # Підключає функцію отримання asgi для застосунку
    'http': get_asgi_application(),
    #
    'websocket': AuthMiddlewareStack( # підключає імпортований клас до вебсокету
        URLRouter(ws_urlpatterns)# підключаємо змінну, у якій створені усі шляхи websocket
    )
})
