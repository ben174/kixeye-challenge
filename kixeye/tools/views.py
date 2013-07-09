from rest_framework import viewsets, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from tools.models import Player, BattleLog
from tools.serializers import PlayerSerializer, BattleLogSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime





def player_list(request):
    """
    List all players, or create a new player.
    """
    if request.method == 'GET':
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PlayerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = create_response()
            return response
        else:
            response = create_response(error=True, msg=str(serializer.errors))
            return response


# this isn't very DRY ... I should have probably made this view 
# handle multiple classes. 
def battle_list(request):
    """
    List all battles, or create a new battle.
    """
    if request.method == 'GET':
        battles = BattleLog.objects.all()
        serializer = BattleLogSerializer(battles, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BattleLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = create_response()
            return response
        else:
            response = create_response(error=True, msg=str(serializer.errors))
            return response


def create_response(error=False, msg=False): 
    ret = { 'time': datetime.datetime.now(), 'error': error, }
    if error: 
        ret['msg'] = msg
    return JSONResponse(ret)


@csrf_exempt
def player_detail(request, pk):
    """
    Retrieve, update or delete a player instance.
    """              
    player = None
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        pass

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        if not player: 
            msg = 'User not found (PK: %s)' % pk
            response = create_response(error=True, msg=msg)
            return response
            
        data = JSONParser().parse(request)
        if not ('field' in data and 'value' in data): 
            msg = 'PUT request must specify a field and value'
            response = create_response(error=True, msg=msg)
            return response
            
        try: 
            setattr(player, data['field'], data['value'])
            player.save()
        except: 
            msg = 'Error setting field %s to value %s' % (
                data['field'], data['value'])
            response = create_response(error=True, msg=msg)
            return response
    
        response = create_response(error=False)
        return response

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
