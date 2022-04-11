from django.db import models


class GameRoom(models.Model):
    room_id = models.IntegerField()
    players = models.TextField(null=True, blank=True)
    players_count = models.IntegerField(null=True, blank=True)
    board = models.TextField(null=True, blank=True)
    playing_player = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Game Room {self.room_id}'
