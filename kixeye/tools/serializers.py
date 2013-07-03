from tools.models import Player, BattleLog
from rest_framework import serializers

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'nickname', )

class BattleLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BattleLog
        fields = ('winner', 'loser')

