#!/usr/bin/env python
import time
import os.path
from os.path import abspath, dirname, join
import sys
import datetime
import re
import random
from rikeripsum import rikeripsum

DIR = dirname(abspath(dirname(__file__)))
sys.path.append(DIR)

from kixeye import settings
from django.core.management import setup_environ

setup_environ(settings)

from tools.models import *
from django.contrib.auth.models import User


adjs = [] 
nouns = []

def main(): 
    create_admin()
    load_words()
    create_random_players(200)


def create_random_players(count): 
    for i in xrange(count): 
        player = Player.objects.create(
            first_name=random.choice(nouns), 
            last_name = random.choice(nouns), 
            nickname = random_username(), 
        )





def create_admin():
    print "Creating user: admin"
    u = User.objects.create_user('admin', 'admin@admin.com', 'changeme')
    u.is_staff = True
    u.is_superuser = True
    u.save()


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return datetime.datetime.date(
        start + datetime.timedelta(seconds=random_second)
    )


def random_username(): 
    return ''.join([random.choice(adjs), random.choice(nouns), random.choice(nouns), 
        str(random.choice(range(18,99)))])


def random_email(username):
    ret = '%s@%s.%s' % (username, random.choice(nouns), random.choice(tlds))
    return ret

def load_words(): 
    global adjs
    global nouns

    f = open('data/adjectives.txt')
    adjs = [l.strip() for l in f.readlines()]

    f = open('data/nouns.txt')
    nouns = [l.strip() for l in f.readlines()]



if __name__ == '__main__': 
    main()
