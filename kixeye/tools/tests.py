from django.test import TestCase
from django.test.client import Client
from tools.models import Player, BattleLog
import json
import datetime


def create_player(first_name, last_name, nickname): 
    player = Player.objects.create(
        first_name=first_name,
        last_name=last_name,
        nickname=nickname,
    )
    return player

class MissionOneTest(TestCase):
    def test_create_user(self):
        """
        Verifies that I can create a user using the REST API. 
        """
        first_name = 'Clark'
        last_name = 'Kent'
        nickname = 'clarkkent'

        # do the POST request
        c = Client()

        post_data = {
            'first_name': first_name,
            'last_name': last_name,
            'nickname': nickname,
        }
        
        response = c.post('/users/', content_type='application/json', 
            data=json.dumps(post_data))
        data = json.loads(response.content)

        player = Player.objects.get(
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
        )
        self.assertEqual(player.nickname, nickname)
        self.assertFalse(data['error'])


    def test_modify_user(self): 
        """
        Verifies that I can modify a user using the REST API. 
        """

        # create original user
        first_name = 'Clark'
        last_name = 'Kent'
        nickname = 'clark_kent'
        player = create_player(first_name, last_name, nickname)
        pk = player.pk

        # do the PUT request
        c = Client()

        put_data = {
            'field': 'nickname',
            'value': 'superman',
        }
        
        response = c.put('/users/%s' % pk, json.dumps(put_data))
        data = json.loads(response.content)

        # verify we didn't return an error
        self.assertFalse(data['error'])

        # retrieve the player from the db
        player = Player.objects.get(pk=pk)

        # verify the modification was made
        self.assertEqual(player.nickname, "superman")

        # verify the original fields are still intact
        self.assertEqual(player.last_name, last_name)


    def test_empty_post(self): 
        """
        Verifies that an empty post fails.
        """
        c = Client()
        response = c.post('/users/', { })
        data = json.loads(response.content)
        self.assertTrue(data['error'])


    def test_create_battle_log(self): 
        """ 
        Verifies that I can create a battle log using the REST API.
        POST /battles
        parameters:
        //Content-Type: application/json
        {
            "attacker": <attacker_userid>,
            "defender": <defender_userid>,
            "winner": <winner_userid>,
            "start": <battle_start_time>,
            "end": <battle_end_time>
        }
        """
        superman, _ = Player.objects.get_or_create(
            first_name = 'Clark', 
            last_name = 'Kent', 
            nickname = 'superman', 
        )

        lex, _ = Player.objects.get_or_create(
            first_name = 'Lex', 
            last_name = 'Luthor', 
            nickname = 'lex_luthor', 
        )

            
        attacker = lex.pk
        defender = superman.pk
        # good always prevails
        winner = superman.pk
        start = datetime.datetime.now() - datetime.timedelta(days=1)
        end = datetime.datetime.now() 

        # do the POST request
        c = Client()

        post_data = {
            'attacker': attacker,
            'defender': defender,
            'winner': winner,
            'start_time': str(start),
            'end_time': str(end),
        }
        
        response = c.post('/battles/', content_type='application/json', 
            data=json.dumps(post_data))
        data = json.loads(response.content)

        battle = BattleLog.objects.get(
            attacker=attacker, 
            defender=defender, 
            winner=winner, 
        )
        # ensure the battle exists and that the winner was superman
        self.assertEqual(battle.winner, Player.objects.get(pk=winner))
        self.assertFalse(data['error'])


    def test_auth(self):
        """
        REQUIREMENT: All API requests MUST BE authenticated using simple username/password authentication.

        Verifies the REST API cannot be accessed anonymously.
        """
        self.assertEqual(1 + 1, 3)


class MissionTwoTest(TestCase): 
    def test_user_profile(self):
        """
        Verifies that I can view a user profile. 
        """
        self.assertEqual(1 + 1, 3)

    def test_user_search(self): 
        """
        Verifies that I can search for a user.
        """
        self.assertEqual(1 + 1, 3)

    def test_battle_logs(self): 
        """
        Verifies that I can search for a user.
        """
        self.assertEqual(1 + 1, 3)

    def test_battle_logs_timerange(self): 
        """
        Verifies that I can search for a user.
        """
        self.assertEqual(1 + 1, 3)


