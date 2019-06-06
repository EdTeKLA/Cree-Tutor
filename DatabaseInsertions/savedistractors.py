from getpass import getpass
import psycopg2
import os
import sys
import re
import unicodedata

#Get db_root, db_pass, and filepaths from settings.py
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'CreeTutorBackEnd'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
import django
django.setup()
from CreeTutorBackEnd import settings_secret

db = None
cursor = None

def connect(user, pw):
    '''
    Function takes in password and connects to database
    Returns None
    '''
    sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'CreeTutorBackEnd'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
    import django
    django.setup()
    global db, cursor
    db = psycopg2.connect(host="localhost", user=user, password=pw, database='cree_tutor_db')
    cursor = db.cursor()

    #MySQL must be reminded many times to use nothing but UNICODE
    #cursor.execute('SET NAMES utf8 COLLATE utf8_bin;')
    #cursor.execute('SET CHARACTER SET utf8;')
    #cursor.execute('SET character_set_connection=utf8;')


    return

def main():
    connect(settings_secret.DB_ROOT, settings_secret.DB_PASS)
    f = open("distractor_type.txt", "r")
    s = "delete from distractor_type"
    cursor.execute(s)
    for line in f:
        line = line.strip('\n')
        spli = line.split(":")
        s = "insert into distractor_type(type, distraction, InSRO) values ({}, '{}', '{}')".format(spli[0], spli[1], spli[2])
        # print(s)
        cursor.execute(s)
    f.close()
    f = open("pair_distractor.txt", "r")
    s = "delete from pair_distractor"
    cursor.execute(s)
    for line in f:
        line = line.strip('\n')
        spli = line.split(":")
        s = "insert into pair_distractor (pair,distractor,type) values ('{}', '{}', {})".format(spli[0], spli[1], spli[2])
        # print(s)
        cursor.execute(s)
    f.close()

    f = open("letter_distractor.txt", "r")
    s = "delete from letter_distractor"
    cursor.execute(s)
    for line in f:
        line = line.strip('\n')
        spli = line.split(":")
        s = "insert into letter_distractor (letter, distractor, type) values ('{}', '{}', {})".format(spli[0], spli[1], spli[2])
        # print(s)
        cursor.execute(s)

    game_levels = {0: 'learn', 1: 'easy', 2: 'medium', 3: 'hard'}
    for key, value in game_levels.items():
        s = "INSERT INTO game_levels(level, name, description) VALUES ('{}', '{}', '{}')".format(key, value, '')
        cursor.execute(s)

    f.close()
    db.commit()
    db.close()

main()
