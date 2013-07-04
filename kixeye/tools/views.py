from django.http import HttpResponse
from tools.models import Player, BattleLog
import datetime
import json



def edit_player(request, player_id): 
    ret = {}
    ret['error'] = False
    ret['time'] = str(datetime.datetime.now())
    if not request.method == "PUT":
        ret['error'] = True
        ret['msg'] = 'Request was not a PUT'
        return HttpResponse(json.dumps(ret), content_type='application/json')

    player = None
    try:    
        player = Player.objects.get(pk=player_id)
    except: 
        ret['error'] = True
        ret['msg'] = 'User with ID %s does not exist.' % player_id
        return HttpResponse(json.dumps(ret), content_type='application/json')

    put_data = None
    print request.body
    
    print "decoding"
    put_data = eval(request.body)
    print "decoding"
    return
    try: 
        put_data = json.loads(str(request.raw_post_data))
    except: 
        ret['error'] = True
        ret['msg'] = 'Error decoding PUT data.'
        return HttpResponse(json.dumps(ret), content_type='application/json')
        
    field = put_data['field']
    value = put_data['value']

    if not field or not value: 
        ret['error'] = True
        ret['msg'] = 'Missing field and/or value.'
        return HttpResponse(json.dumps(ret), content_type='application/json')

    try: 
        player.__dict__[field] = value
        player.save()
    except Exception, e: 
        ret['error'] = True
        ret['msg'] = str(e)

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
        ret['msg'] = 'Error saving Player'

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
