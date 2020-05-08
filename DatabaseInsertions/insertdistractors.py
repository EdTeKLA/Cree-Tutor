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
    """
    Function takes in password and connects to database
    Returns None
    """

    global db, cursor
    db = psycopg2.connect(host="localhost", user=user, password=pw, database='cree_tutor_db')
    cursor = db.cursor()

    #MySQL must be reminded many times to use nothing but UNICODE
    #cursor.execute('SET NAMES utf8 COLLATE utf8_bin;')
    #cursor.execute('SET CHARACTER SET utf8;')
    #cursor.execute('SET character_set_connection=utf8;')


    return

def letter_distractors():
    f = open("letter_distractor.txt", "r")
    for line in f:
        line = line.split(":")
        letter = line[0].strip()
        distractor = line[1].strip()
        type = line[2].strip()
        if len(line) == 3:
            e = "INSERT INTO ai(distractor, type, letter) VALUES ('{}', '{}', '{}')".format(distractor, type, letter)
            cursor.execute(e)

    db.commit()

    return

def pair_distractors():
    f.open("pair_distractor.txt", "r")
    for line in f:
        line = line.split(":")
        letter = line[0].strip()
        distractor = line[1].strip()
        type = line[2].strip()
        if len(line) == 3:
            e = "INSERT INTO pair_distractor ('{}', '{}', '{}')".format(distractor, type, letter)
            cursor.execute(e)

    db.commit()

    return

def main():
    connect(settings_secret.DB_ROOT, settings_secret.DB_PASS)
    letter_distractors()
    pair_distractors()
    db.commit()
    db.close()

    return


main()
