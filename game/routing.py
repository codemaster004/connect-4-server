from django.urls import path
from .consumer import Connect4Consumer


websocket_urlpatterns = [
    path('ws/play/<int:room_code>/', Connect4Consumer.as_asgi()),
]
