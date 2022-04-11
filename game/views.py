from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse

from .models import GameRoom

import json


def index(request):
    if request.method == 'POST':
        room_code = request.POST.get("room_code")
        char_choice = request.POST.get("character_choice")

        return redirect(f'/play/{room_code}?&choice={char_choice}')
    return render(request, 'game/index.html', {})


def game(request, room_code):
    choice = request.GET.get("choice")
    if choice not in ['X', 'O']:
        raise Http404("Choice does not exists")

    context = {
        "char_choice": choice,
        "room_code": room_code
    }
    return render(request, "game/game.html", context)


def room_status(request, room_code):

    players = []

    room_objects = GameRoom.objects.filter(room_id=room_code)
    if len(room_objects) == 0:
        room = GameRoom.objects.create(room_id=room_code)
        room.players_count = 0
        room.players = json.dumps([])
        room.save()
    else:
        room = room_objects[0]
        if room.players != '':
            players = json.loads(room.players)

    return HttpResponse(json.dumps({'players': players}), content_type='application/json')


