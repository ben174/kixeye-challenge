from tools.models import Player, BattleLog
from rest_framework import serializers
import datetime

class PlayerSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(required=True, max_length=100)
    first_name = serializers.CharField(required=True, max_length=100)
    nick_name = serializers.CharField(required=True, max_length=100)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.nickname = attrs.get('nickname', instance.nickname)
            return instance
        return Player(**attrs)

    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'nickname', )


class BattleLogSerializer(serializers.ModelSerializer):
    attacker = serializers.IntegerField(required=True)
    defender = serializers.IntegerField(required=True)
    winner = serializers.IntegerField(required=True)
    start_time = serializers.DateTimeField(required=True)
    end_time = serializers.DateTimeField(required=True)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.attacker = attrs.get('attacker', instance.attacker)
            instance.defender = attrs.get('defender', instance.defender)
            instance.winner = attrs.get('winner', instance.winner)
            instance.start_time = attrs.get('start_time', instance.start_time)
            instance.end_time = attrs.get('end_time', instance.end_time)
            return instance
        player = BattleLog(
            attacker=Player.objects.get(pk=attrs['attacker']),
            defender=Player.objects.get(pk=attrs['defender']),
            winner=Player.objects.get(pk=attrs['winner']),
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
        )
        return player
    class Meta:
        model = BattleLog
        fields = ('attacker', 'defender', 'winner', 'start_time', 'end_time')

