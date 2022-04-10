from django.urls import path
from .consumer import TicTacToeConsumer


websocket_urlpatterns = [
    path('ws/play/<int:room_code>/', TicTacToeConsumer.as_asgi()),
]
