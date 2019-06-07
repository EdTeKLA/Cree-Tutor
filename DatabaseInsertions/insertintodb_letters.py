from getpass import getpass
import MySQLdb
import os
import sys

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
    Cycles through directory and extracts individual names and paths. Inserts names and paths pre-made Alphabet table
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
            executestring = "INSERT INTO alphabet VALUES ('{}','','{}')".format(new, finalpath)
            print(executestring)
            cursor.execute(executestring)

    db.commit()
    return


def namevowel():
    """
    Function takes in no arguments.
    Function executes SQL script to update the vowel state of the vowels inserted into the database by
    cyclethru.
    Returns nothings.
    """

    vowels = ['a', 'e', 'i', 'o']
    for v in vowels:
        executestring = "UPDATE Alphabet SET vowel = 'vowel' where name like '%{}%'".format(v)
        print(executestring)
        cursor.execute(executestring)

    db.commit()
    return

def semivowel():
    """
    Function takes in no arguments.
    Function executes SQL script to update the vowel state of the semivowels inserted into the database by
    cyclethru.
    Returns nothings.
    """

    executestring = "UPDATE Alphabet SET vowel = 'semivowel' where name = 'y' or name = 'w'"
    print(executestring)
    cursor.execute(executestring)

    db.commit()
    return

def consonant():
    """
    Function takes in no arguments.
    Function executes SQL script to update the vowel state of the consonants inserted into the database by
    cyclethru.
    Returns nothings.
    """

    executestring = "UPDATE Alphabet SET vowel = 'consonant' where vowel = ''"
    print(executestring)
    cursor.execute(executestring)

    db.commit()
    return


def main():
    global db

    db = input("Please enter the name of your database: ")
    password = getpass()
    connect(password)

    executestring = "Delete from Alphabet"
    cursor.execute(executestring)
    db.commit()

    directory = input('Drag the file of alphabet sounds here now: ')
    cyclethru(directory)
    namevowel()
    semivowel()
    consonant()

    db.close()

    return


main()
