from getpass import getpass
import MySQLdb
import os
import sys
import re

db = None
cursor = None

def connect(user, pw):
    '''
    Function takes in password and connects to database
    Returns None
    '''

    global db, cursor
    db = MySQLdb.connect("localhost", user, pw, 'CreeTutordb' )
    db.set_character_set('utf8')
    cursor = db.cursor()

    #MySQL must be reminded many times to use nothing but UNICODE 
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    return

def dbInfo():
    user = input("Please enter the name of your database user (e.g. root): ")
    password = getpass()

    connect(user, password)

    while True:
        print("Are you\n1.Adding new data\n2.Re-populating the database?\n(1/2):")
        delete = input()
        if delete == '1':
            break
        elif delete == '2':
            emptyDb()
            break
        else:
            print("That is not valid input")

    return


def emptyDb():
    # THIS ORDER MATTERS. letter_pair has foreign keys that reference alphabet, and mysql will throw a key error otherwise
    cursor.execute("delete from letter_pair")
    cursor.execute("delete from alphabet")
    cursor.execute("delete from word")
    db.commit()

    return


def cycleSound(directory_in_str):
    '''
    Function takes in a string path to the desired directory. Directory must be in static folder of django project.
    Cycles through directory and extracts individual pairs and paths. Passes pair to getfirstsecond to identify the first
    and second letter of the letter pair, and return them.
    Inserts names, first letters, second letters, and paths into pre-made Alphabet table
    in database.
    Returns None
    '''

    # Cycle through directory
    directory = os.fsencode(directory_in_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # TODO: Currently hardcoded to only allow wav files
        if filename.endswith(".wav") or filename.endswith(".m4a"):
            pathname = os.path.join(directory, file)
            finalpath = os.fsdecode(pathname)
            finalpath = finalpath.replace("\\", "/")
            # Splits on 'static/' so that path string is appropriate for django to read
            finalpath = finalpath.split('static/')[1]
            new = filename.replace('.wav', '')
            new = new.replace('.m4a', '')
            if "._" in new:
                continue
            first, second = getfirstsecond(new)
            getfirstsecond(new)
            executestring = "INSERT INTO letter_pair VALUES ('{}','{}','{}','{}')".format(new, first, second, finalpath)
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

        # else:
        #     sys.exit("False pair")

    return first, second

def cycleWords(directory_in_str):
    '''
    Function takes in a string path to the desired directory. Directory must be in static folder of django project.
    Cycles through directory and extracts individual names and paths. Passes individual names to function syllables to count the
    number of syllables in word. Inserts names, paths, number of syllables, and an id into pre-made word table
    in database. Strips names of any non-alpha character and does not allow names with whitespace or duplicate names.
    Returns None
    '''

    word_id = 0
    executestring = "INSERT INTO word VALUES"
    directory = os.fsencode(directory_in_str)

    # Cycle through directory
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        # TODO: Currently hardcoded to only allow wav files
        if filename.endswith(".wav") or filename.endswith(".m4a"):
            pathname = os.path.join(directory, file)
            finalpath = os.fsdecode(pathname)
            finalpath = finalpath.replace("\\", "/")
            # Splits on 'static/' so that path string is appropriate for django to read
            finalpath = finalpath.split('static/')[1]
            new = filename.replace('.wav', '').lower()
            new = new.replace('.m4a', '').lower()
            if "._" in new:
                continue
            # If exists whitespace, then not a single word
            if ' ' in new:
                continue
            # Strip word of any underscores or digits
            new = re.sub('[^A-Za-z`̂]', '', new)
            # If name already in execution string, then skip to avoid duplicates
            if "'{}',".format(new) in executestring:
                continue
            num_syllables = syllables(new)
            executestring += "({},'{}', NULL, NULL, {}, NULL),".format(word_id, new, num_syllables)
            word_id +=1

    executestring = executestring[0:-1]
    # print(executestring)
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

def cycleLetters(directory_in_str):
    '''
    Function takes in a string path to the desired directory. Directory must be in static folder of django project.
    Cycles through directory and extracts individual names and paths. Inserts names and paths pre-made Alphabet table
    in database.
    Returns None
    '''

    # Cycle through directory
    directory = os.fsencode(directory_in_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # TODO: Currently hardcoded to only allow wav files
        if filename.endswith(".wav") or filename.endswith(".m4a"):
            pathname = os.path.join(directory, file)
            finalpath = os.fsdecode(pathname)
            finalpath = finalpath.replace("\\", "/") # Accounts for Windows machines
            # Splits on 'static/' so that path string is appropriate for django to read
            finalpath = finalpath.split('static/')[1]
            new = filename.replace('.wav', '')
            new = new.replace('.m4a', '')
            if "._" in new:
                continue
            executestring = "INSERT INTO alphabet VALUES ('{}','','{}')".format(new, finalpath)
            print(executestring)
            cursor.execute(executestring)

    db.commit()
    namevowel()
    semivowel()
    consonant()
    return


def namevowel():
    '''
    Function takes in no arguments.
    Function executes SQL script to update the vowel state of the vowels inserted into the database by
    cyclethru.
    Returns nothings.
    '''

    vowels = ['a', 'e', 'i', 'o']
    for v in vowels:
        executestring = "UPDATE Alphabet SET vowel = 'vowel' where letter like '%{}%'".format(v)
        cursor.execute(executestring)

    db.commit()
    return

def semivowel():
    '''
    Function takes in no arguments.
    Function executes SQL script to update the vowel state of the semivowels inserted into the database by
    cyclethru.
    Returns nothings.
    '''

    executestring = "UPDATE Alphabet SET vowel = 'semivowel' where letter = 'y' or letter = 'w'"
    cursor.execute(executestring)

    db.commit()
    return

def consonant():
    '''
    Function takes in no arguments.
    Function executes SQL script to update the vowel state of the consonants inserted into the database by
    cyclethru.
    Returns nothings.
    '''

    executestring = "UPDATE Alphabet SET vowel = 'consonant' where vowel = ''"
    cursor.execute(executestring)

    db.commit()
    return

def main():

    dbInfo()

    word = input("Please enter the path to 'word' recordings: ")
    print("\n")
    alphabet = input("Please enter the path to 'alphabet' recordings: ")
    print("\n")
    sound = input("Please enter the path to 'letter pair' recordings: ")

    cycleWords(word)
    cycleLetters(alphabet)
    cycleSound(sound)

    db.commit()
    db.close()

    return


main()
