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

def cyclethru(directory_in_str):
    """
    Function takes in a string path to the desired directory. Directory must be in static folder of django project.
    Cycles through directory and extracts individual names and paths. Passes name to getfirstsecond to identify the first
    and second letter of the letter pair, and return them.
    Inserts names, first letters, second letters, and paths into pre-made Alphabet table
    in database.
    Returns None
    """

    # Cycle through directory
    directory = os.fsencode(directory_in_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # TODO: Currently hardcoded to only allow wav files
        if filename.endswith(".wav"):
            pathname = os.path.join(directory, file)
            finalpath = os.fsdecode(pathname)
            # Splits on 'static/' so that path string is appropriate for django to read
            finalpath = finalpath.split('static/')[1]
            new = filename.replace('.wav', '')
            first, second = getfirstsecond(new)
            getfirstsecond(new)
            executestring = "INSERT INTO letter_pairs VALUES ('{}','{}','{}','{}')".format(new, first, second, finalpath)
            print(executestring)
            cursor.execute(executestring)

    db.commit()
    return


def getfirstsecond(pair):
    if len(pair) == 2:
        first = pair[0]
        second = pair[1]
    else:
        m = re.match('(\w\W)(\w)', pair)
        n = re.match('(\w)(\w\W)', pair)

        if m!= None:
            first = m.group(1)
            second = m.group(2)

        elif n!= None:
            first = n.group(1)
            second = n.group(2)

        else:
            sys.exit("False pair")

    return first, second


def main():
    global db

    db = input("Please enter the name of your database: ")
    password = getpass()
    connect(password)

    executestring = "Delete from letter_pairs"
    cursor.execute(executestring)

    db.commit()
    directory = input('Drag the file of letter pair sounds here now:')
    cyclethru(directory)



    db.close()

    return


main()
