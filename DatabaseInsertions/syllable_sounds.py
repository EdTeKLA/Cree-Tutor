from getpass import getpass
import MySQLdb
import os
import sys
import re

db = None
cursor = None

def connect():
    """
    Function takes in password and connects to database
    Returns None
    """

    global db, cursor
    db = MySQLdb.connect("localhost","root", '2718nehiyawewin', 'CreeTutordb' )
    cursor = db.cursor()
    return


def sylgame():
    executestring = "DELETE FROM sound_in_syl"
    cursor.execute(executestring)
    db.commit()


    executestring = "SELECT word_id, word from words"
    cursor.execute(executestring)
    f = cursor.fetchall()
    for i in f:
        executestring = "SELECT syllable_name, id from word_syllables where word_id = {}".format(i[0])
        cursor.execute(executestring)
        g = cursor.fetchall()
        for j in g:
            m = re.findall('[aieo`̂][aieo`̂]?[wy]', j[0])
            n = re.findall('[aieo`̂][aieo`̂]?', j[0])
            if m:
                return m[0], n[0]
            else:
                s = ''
                return s, n[0]






def main():
    connect()
    sylgame()


main()
