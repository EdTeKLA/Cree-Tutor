from getpass import getpass
import MySQLdb
import os
import sys
import re
import unicodedata

db = None
cursor = None

def connect(user, pw):
    '''
    Function takes in password and connects to database
    Returns None
    '''

    global db, cursor
    db = MySQLdb.connect("localhost", "root", "2240498", 'CreeTutordb' )
    db.set_character_set('utf8')
    cursor = db.cursor()

    #MySQL must be reminded many times to use nothing but UNICODE
    #cursor.execute('SET NAMES utf8 COLLATE utf8_bin;')
    #cursor.execute('SET CHARACTER SET utf8;')
    #cursor.execute('SET character_set_connection=utf8;')


    return

def letter_distractors():
    f.open("letter_distractor.txt", "r")
    for line in f:
        line = line.split(":")
        letter = line[0].strip()
        distractor = line[1].strip()
        type = line[2].strip()
        if len(line) == 3:
            e = "INSERT INTO letter_distractor ('{}', '{}', '{}')".format(distractor, type, letter)
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
    connect("root", "pw")
    letter_distractors()
    pair_distractors()
    db.commit()
    db.close()

    return


main()
