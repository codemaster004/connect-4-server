from django.db import models


class GameRoom(models.Model):
    room_id = models.IntegerField()
    players = models.TextField()
    players_count = models.IntegerField()
    board = models.TextField()
    playing_player = models.TextField()
