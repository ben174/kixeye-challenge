from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.contrib.auth.management import create_superuser
from django.contrib.auth import models as auth_app
import datetime

'''
# Prevent interactive question about wanting a superuser created.
signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_app,
    dispatch_uid = "django.contrib.auth.management.create_superuser"
)
'''

class Player(models.Model): 
    """ A class to hold a Player, which is anyone who plays one of 
    our awesome online games. 
    """
    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    nickname = models.CharField(
        max_length=100,
        unique=True,
        null=False, 
        blank=False,
    )

    win_count = models.IntegerField(
        default=0,
        null=False, 
        blank=False,
    )

    loss_count = models.IntegerField(
        default=0,
        null=False, 
        blank=False,
    )

    win_streak = models.IntegerField(
        default=0,
        null=False, 
        blank=False,
    )

    created = models.DateTimeField(
        auto_now_add = True, 
    )

    # how should this be populated? not on save, because that doesn't 
    # necessarily indicate that the user has logged in (could be a batch
    # process, etc.
    last_seen = models.DateTimeField(
        auto_now_add = True, 
    )


    def user_did_battle(self, user_won=False): 
        if user_won: 
            self.win_count += 1
            self.win_streak += 1
        else: 
            self.loss_count += 1 
            self.win_streak = 0
        self.save()

    def __unicode__(self): 
        return "%s" % (self.nickname)


class BattleLog(models.Model): 
    """ An instance of a battle which occurred.
    """
    attacker = models.ForeignKey(
        'Player', 
        null=False, 
        related_name='initiated_battles', 
    )

    defender = models.ForeignKey(
        'Player', 
        null=False, 
        related_name='defended_battles', 
    )

    # I considered making this a char field holding either 'A' for 
    # attacker or 'D' for defender. Or even a boolean field named
    # attacker_won. But I decided against it because then you don't 
    # Have the ability to say battle_log.winner.first_name, etc. 
    # Instead, I added a save constraint to prevent adding a winner 
    # who didn't play. 
    winner = models.ForeignKey(
        'Player', 
        null=False, 
        related_name='victorious_battles', 
    )

    start_time = models.DateTimeField(
        null=False, 
        blank=False, 
    )

    end_time = models.DateTimeField(
        null=False, 
        blank=False, 
    )

    def save(self):
        if (self.winner.pk != self.attacker.pk) and (
            self.winner.pk != self.defender.pk): 
            raise Exception("Winner must have been in the battle.")
        # trigger user_did_battle, which increments/resets win counts
        self.winner.user_did_battle(user_won=True)
        if self.winner == self.attacker: 
            self.defender.user_did_battle(user_won=False)
        else: 
            self.attacker.user_did_battle(user_won=False)
        super(BattleLog, self).save()

