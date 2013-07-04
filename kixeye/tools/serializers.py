from tools.models import Player, BattleLog
from rest_framework import serializers

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    last_name = serializers.CharField(required=False, max_length=100)
    first_name = serializers.CharField(required=False, max_length=100)
    nick_name = serializers.CharField(required=False, max_length=100)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.nickname = attrs.get('nickname', instance.nickname)
            return instance
        return Snippet(**attrs)

    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'nickname', )


class BattleLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BattleLog
        fields = ('winner', 'loser')

