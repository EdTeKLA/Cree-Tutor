from getpass import getpass
import MySQLdb
import os
import sys
import re

db = None
cursor = None

def connect(pw):
    '''
    Function takes in password and connects to database
    Returns None
    '''

    global db, cursor
    db = MySQLdb.connect("localhost","root", pw, db )
    cursor = db.cursor()
    return


def cyclethru(directory_in_str):
    '''
    Function takes in a string path to the desired directory. Directory must be in static folder of django project.
    Cycles through directory and extracts individual names and paths. Passes individual names to function syllables to count the
    number of syllables in word. Inserts names, paths, number of syllables, and an id into pre-made words table
    in database. Strips names of any non-alpha character and does not allow names with whitespace or duplicate names.
    Returns None
    '''

    word_id = 0
    executestring = "INSERT INTO words VALUES"
    directory = os.fsencode(directory_in_str)

    # Cycle through directory
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        # TODO: Currently hardcoded to only allow wav files
        if filename.endswith(".wav"):
            pathname = os.path.join(directory, file)
            finalpath = os.fsdecode(pathname)
            # Splits on 'static/' so that path string is appropriate for django to read
            finalpath = finalpath.split('static/')[1]
            new = filename.replace('.wav', '').lower()
            # If exists whitespace, then not a single word
            if ' ' in new:
                continue
            # Strip word of any underscores or digits
            new = re.sub('[^A-Za-z`̂]', '', new)
            # If name already in execution string, then skip to avoid duplicates
            if "'{}',".format(new) in executestring:
                continue
            num_syllables = syllables(new)
            executestring += "('{}','{}','{}'),".format(new, word_id, num_syllables)
            word_id +=1

    executestring = executestring[0:-1]
    cursor.execute(executestring)
    db.commit()
    return

def syllables(word):
    '''
    Function takes in word string and counts the number of syllables.
    Returns int, number of syllables
    Ref: https://stackoverflow.com/questions/46759492/syllable-count-in-python
    '''

    # TODO: Consider whether 'ew' counts as two syllables

    count = 0
    vowels = 'aeioâîô'
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if count == 0:
        count +=1

    return count


def main():
    global db

    db = input("Please enter the name of your database: ")
    password = getpass()
    connect(password)

    executestring = "Delete from words"
    cursor.execute(executestring)
    db.commit()

    directory = input('Drag the file of word sounds here now: ')
    cyclethru(directory)

    db.close()

    return


main()
