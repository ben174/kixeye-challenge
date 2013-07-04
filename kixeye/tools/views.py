from django.http import HttpResponse
from tools.models import Player, BattleLog
import datetime
import json



def player(request, player_id): 
    ret = {}
    ret['error'] = False
    print "PLAY %s " % player_id
    ret = "DONE" 
    return HttpResponse(json.dumps(ret), content_type='application/json')


def player(request): 
    ret = {}
    ret['error'] = False
    ret['time'] = str(datetime.datetime.now())
    player = None
    if not request.POST: 
        ret['error'] = True
        ret['msg'] = 'Request was not a POST'
    else: 
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        nickname = request.POST.get('nickname', None)
        try: 
            player = create_player(first_name, last_name, nickname)
        except Exception, e: 
            ret['error'] = True
            ret['msg'] = str(e)

    if player: 
        ret['userid'] = player.pk
    else: 
        ret['error'] = True
        ret['error'] = 'Error saving Player'

    return HttpResponse(json.dumps(ret), content_type='application/json')


def create_player(first_name, last_name, nickname): 
    player = Player.objects.create(
        first_name=first_name,
        last_name=last_name,
        nickname=nickname,
    )
    return player


def battle_log(request): 
    if request.POST: 
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        nickname = request.POST.get('nickname')
        player = Player.objects.create(
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
        )
        player.save()

    return HttpResponse("done")
