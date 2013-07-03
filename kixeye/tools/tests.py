from django.test import TestCase
import urllib2


def create_user(first_name, last_name, nickname): 
    pass

class MissionOneTest(TestCase):
    def test_create_user(self):
        """
        Verifies that I can create a user using the REST API. 
        """
        #c = Client()
        #c.post('/users/', {'first': 'fred', 'last': 'secret', 'nickname': ''})
        self.assertEqual(1 + 1, 3)

    def test_create_user(self):
        """
        Verifies that I can modify a user using the REST API. 
        """
        self.assertEqual(1 + 1, 3)

    def test_create_battle_log(self): 
        """ 
        Verifies that I can create a battle log using the REST API.
        """
        self.assertEqual(1 + 1, 3)

    def test_auth(self)
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


