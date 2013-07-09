from rest_framework import viewsets, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, \
    authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework import permissions
from tools.models import Player, BattleLog
from tools.serializers import PlayerSerializer, BattleLogSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404  
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db.models import Q
import datetime


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes((BasicAuthentication,))
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def player_list(request):
    """
    List all players, or create a new player.
    """
    if request.method == 'GET':
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = None
        try: 
            data = JSONParser().parse(request)
            serializer = PlayerSerializer(data=data)
        except: 
            response = create_response(error=True, msg="Invalid post data")
            return response
        if serializer.is_valid():
            serializer.save()
            response = create_response()
            return response
        else:
            response = create_response(error=True, msg=str(serializer.errors))
            return response


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes((BasicAuthentication,))
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def battle_list(request):
    """
    List all battles, or create a new battle.
    """
    if request.method == 'GET':
        # dates are never fun in urls. I'm going to go with YYYY-MM-DD
        start_time_string = request.GET.get('start', None)
        end_time_string = request.GET.get('end', None)
        start_time = parse_date_string(start_time_string)
        end_time = parse_date_string(end_time_string)
        q = Q()
        if start_time: 
            q &= Q(start_time__gte=start_time)
        if end_time: 
            q &= Q(end_time__lte=end_time)
        battles = BattleLog.objects.filter(q)
        return render(request, 'battles.html', { 
            'start_time': start_time,
            'end_time': end_time,
            'battles': battles,
        })

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


@csrf_exempt
@api_view(['GET', 'PUT'])
@authentication_classes((BasicAuthentication,))
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def player_detail(request, pk):
    """
    Retrieve or update a player instance.
    """              
    player = None
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        pass

    if request.method == 'GET':
        return render(request, 'player.html', { 'player': player })

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


def player_search(request): 
    """ 
    Search for a player and resolve it to its proper url.
    """
    nickname = request.GET.get('nickname')
    try: 
        player = Player.objects.get(nickname=nickname)
    except Player.DoesNotExist:
        raise Http404
    return HttpResponseRedirect('/users/%s' % player.pk)


def create_response(error=False, msg=False): 
    ret = { 'time': datetime.datetime.now(), 'error': error, }
    if error: 
        ret['msg'] = msg
    return JSONResponse(ret)


def parse_date_string(date_string): 
    try: 
        y,m,d = date_string.split('-')
        return datetime.date(int(y),int(m),int(d))
    except:
        return None


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

