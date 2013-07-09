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
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404  
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db.models import Q
import datetime


def player_search(request): 
    nickname = request.GET.get('nickname')
    try: 
        player = Player.objects.get(nickname=nickname)
    except Player.DoesNotExist:
        raise Http404
    return HttpResponseRedirect('/users/%s' % player.pk)


def player_list(request):
    """
    List all players, or create a new player.
    """
    # Challenge requirements were a bit strange on this one, but I decided to take 
    # them literally.  
    # Based on the specifications, a POST to /users/<pk> should create a user, 
    # but a GET should return a profile page. If I were designing specs, 
    # I'd probably create unique URLS for each, to avoid confusion.
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


def parse_date_string(date_string): 
    try: 
        y,m,d = date_string.split('-')
        return datetime.date(int(y),int(m),int(d))
    except:
        return None

# this isn't very DRY ... I should have probably made this view 
# handle multiple classes. 
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


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

