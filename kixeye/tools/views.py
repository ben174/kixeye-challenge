from rest_framework import viewsets
from tools.models import Player, BattleLog
from tools.serializers import PlayerSerializer, BattleLogSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed or edited.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class BattleLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows battle logs to be viewed or edited.
    """
    queryset = BattleLog.objects.all()
    serializer_class = BattleLogSerializer

