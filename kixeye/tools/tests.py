from django.test import TestCase
from django.test.client import Client
from tools.models import Player
import json


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
        c = Client()
        first_name = 'Clark'
        last_name = 'Kent'
        nickname = 'ckent'
        response = c.post('/player/', {
            'first_name': first_name,
            'last_name': last_name,
            'nickname': nickname,
        })
        player = Player.objects.get(
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
        )
        data = json.loads(response.content)
        self.assertEqual(player.nickname, nickname)
        self.assertFalse(data['error'])


    def test_modify_user(self): 
        """
        Verifies that I can modify a user using the REST API. 
        """

        # create original user
        first_name = 'Clark'
        last_name = 'Kent'
        nickname = 'ckent'
        player = create_player(first_name, last_name, nickname)
        pk = player.pk

        # do the modification
        c = Client()
        response = c.put('/player/%s' % pk, {
            'field': 'nickname',
            'value': 'superman',
        })
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
        response = c.post('/player/', { })
        data = json.loads(response.content)
        self.assertTrue(data['error'])


    def test_create_battle_log(self): 
        """ 
        Verifies that I can create a battle log using the REST API.
        """
        self.assertEqual(1 + 1, 3)

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


