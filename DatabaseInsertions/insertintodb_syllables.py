from getpass import getpass
import MySQLdb
import os
import sys
import re

db = None
cursor = None

def connect(pw):
    """
    Function takes in password and connects to database
    Returns None
    """

    global db, cursor
    db = MySQLdb.connect("localhost","root", pw, db )
    cursor = db.cursor()
    return

def getwords():
    id = 0
    executestring = "SELECT word, word_id FROM words;"
    cursor.execute(executestring)
    fetched = cursor.fetchall()
    for words in fetched:
        syldic = getsyllables(words[0])
        for i in syldic:
            pair, vowel = sylsound(syldic[i])
            executestring = "INSERT INTO word_syllables VALUES({}, {}, '{}', {}, '{}', '{}');".format(words[1], i, syldic[i], id, pair, vowel)
            id += 1
            cursor.execute(executestring)
    db.commit()
    return

def getsyllables(word):
    n = re.findall('[^aeio`̂]?[aeio`̂]+[^aeio`̂]*', word)
    count = 1
    sylls = dict()
    for i in n:
        sylls[count] = i
        count += 1

    return sylls

def sylsound(syl):
    m = re.findall('[aieo`̂][aieo`̂]?[wy]', syl)
    n = re.findall('[aieo`̂][aieo`̂]?', syl)
    if m:
        return m[0], n[0]
    else:
        s = ''
        return s, n[0]

def main():
    global db

    db = input("Please enter the name of your database: ")
    password = getpass()
    connect(password)

    executestring = "Delete from word_syllables"
    cursor.execute(executestring)
    db.commit()
    getwords()

main()
