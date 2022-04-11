from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import GameRoom

import json
from threading import Thread


def add_player(roomNumber, new_player):
    room = GameRoom.objects.get(room_id=roomNumber)
    if room.players != '':
        players = json.loads(room.players)
    else:
        players = []
    players.append(new_player)
    room.players = json.dumps(players)
    room.players_count += 1
    room.save()


class Connect4Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name
        print(f'Connected to room {self.room_name}')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        action = response.get("action", None)
        message = response.get("message", None)
        print(f'{event=}', response)

        if event == 'MOVE':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'action': action,
                'message': message,
                'event': 'MOVE'
            })

        if event == 'RESET':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': action,
                'event': 'RESET'
            })

        if event == 'JOIN':
            new_player = action['player']
            Thread(target=add_player, args=(self.room_name, new_player)).start()

            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'action': action,
                'message': message,
                'event': 'JOIN'
            })

        if event == 'END':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': action,
                'event': "END"
            })

    async def send_message(self, res):
        """ Receive message from room group """

        await self.send(text_data=json.dumps({
            "payload": res,
        }))
