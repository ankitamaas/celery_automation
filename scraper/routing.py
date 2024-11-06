from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/notification/', consumer.FrontendConsumer.as_asgi()),
]