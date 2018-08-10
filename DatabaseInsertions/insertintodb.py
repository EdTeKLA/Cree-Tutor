from getpass import getpass
import MySQLdb
import os
import sys
import re
import unicodedata

db = None
cursor = None

#Set filenames
GRAMCODE_FILENAME = 'gram_codes.txt'
LEMMA_FILENAME = 'lemmas.txt'
WORDS_FILENAME = 'words_for_db.txt'

#Get db_root, db_pass, and filepaths from settings.py
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'CreeTutorBackEnd'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
import django
django.setup()
from CreeTutorBackEnd import settings



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
    #cursor.execute('SET NAMES utf8 COLLATE utf8_bin;')
    #cursor.execute('SET CHARACTER SET utf8;')
    #cursor.execute('SET character_set_connection=utf8;')


    return

def dbInfo():
    #user = input("Please enter the name of your database user (e.g. root): ")
    #password = getpass()

    #connect(user, password)
    connect(settings.DB_ROOT, settings.DB_PASS)

    # while True:
    #     print("Are you\n1.Adding new data\n2.Re-populating the database?\n(1/2):")
    #     delete = input()
    #     if delete == '1':
    #         break
    #     elif delete == '2':
    #         emptyDb()
    #         break
    #     else:
    #         print("That is not valid input")

    emptyDb()

    return


def emptyDb():
    # THIS ORDER MATTERS. letter_pair has foreign keys that reference alphabet, and mysql will throw a key error otherwise
    cursor.execute("delete from letter_pair")
    cursor.execute("delete from alphabet")
    cursor.execute("delete from word")
    cursor.execute("delete from lemma")
    cursor.execute("delete from gram_code")



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
            new = unicodedata.normalize('NFKC', new)
            first = unicodedata.normalize('NFKC', first)
            second = unicodedata.normalize('NFKC', second)
            executestring = "INSERT INTO letter_pair VALUES ('{}','{}','{}','{}')".format(new, finalpath, first, second)
            cursor.execute(executestring)

    db.commit()
    return


def getfirstsecond(pair):
    if len(pair) == 2:
        first = pair[0]
        second = pair[1]
    else:
        #if the accent (\W) is on the first letter
        m = re.match('(\w\W)(\w)', pair)
        #if the accent (\W) is on the second letter
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

def cycleWords(directory_in_str, lemma_dict):
    """
    Opens Linguistics/words_for_db.txt
    Adds entry for each line in words_for_db.txt
        A line looks like this:
    acimosis	N+AN+Der/Dim+N+AN+Sg	puppy	      atim	acimosis.wav
    word        gram_code               translation   lemma filename.wav,other_file.mp4
        Columns are seperated by tab (\t). Note that atom hates typing \t.
        Be careful using atom to edit words_for_db.txt
    """


    word_id = 0
    executestring = "INSERT INTO word VALUES"
    directory = directory_in_str

    #read in file
    with open(os.path.join(directory,WORDS_FILENAME), 'r') as readfile:
        word_lines = readfile.readlines()

    #cycle through lines
    count = 0
    for e in word_lines:
        #No double characters! No other funny business!
        content = unicodedata.normalize("NFKC", e)
        #Split the columns into a list
        content_as_list = content.split('\t')
        #If there aren't enough columns, print which word caused the failure
        #One will need to go through words_for_db and find out why.
        #DON"T USE ATOM FOR THIS PART! Atom hates \t.
        if len(content_as_list) != 5:
            sys.stdout.write(
                                "Error on line " + str(word_id) + '\n' +
                                str(content_as_list) + '\n'
                                )
            break
        else:
            #get the stuff, man
            word = content_as_list[0]
            gram_code = content_as_list[1]
            #print([ord(e) for e in gram_code])
            if gram_code == '':
                gram_code = 'NULL'
            translation = content_as_list[2]
            lemma = content_as_list[3]
            #make sure lemma is already in the db


            #find the lemma in the Lemma table
            cursor.execute("SELECT lemma FROM Lemma")
            f = cursor.fetchall()
            for i in f:
                # fetchall returns everything as a tuple, i.e. of the form ('lemma',)
                if lemma == i[0]:
                    pass
                    #print("Lemma " + str(lemma) + " is in the DB")

            #find the lemma in the Lemma table
            e = "SELECT * from gram_code where gram_code = '{}'".format(gram_code)
            cursor.execute(e)
            f = cursor.fetchone()
            # for i in f:
            #     # fetchall returns everything as a tuple, i.e. of the form ('lemma',)
            #     if gram_code == i[0]:
            #         print("Gram_CODE " + str(gram_code) + " is in the DB")
            if not f:
                print(gram_code + " is not in the db")

            #TODO for now, just save the first audio file. Eventually all.
            audio_files = content_as_list[4].split(',')[0]

            #get number of syllables
            num_syllables = syllables(word)



            add_to_executestring = "('{}', '{}', '{}', '{}', '{}', '{}', '{}'),".format(
                word_id,
                word,
                translation,
                num_syllables,
                audio_files,
                lemma_dict[lemma],
                gram_code,
                )

            if word_id == 0:
                print(add_to_executestring)
            executestring = "INSERT INTO word(word_id, word, translation, num_syllables, sound, lemmaID_id, gram_code_id) VALUES"
            executestring += add_to_executestring
            executestring = executestring.replace("\n", "")
            executestring = executestring[0:-1]
            try:
                cursor.execute(executestring)
            except:
                print(executestring)
                count += 1

            word_id +=1

    #chop off the trailing comma
    print("Number of fails: " + str(count))
    # executestring = executestring[0:-1]
    # #print(executestring)
    # executestring = executestring.replace("\n", "")
    # cursor.execute(executestring)
    db.commit()
    return

""" Delaneys cycleWords
    '''
    Function takes in a string path to the desired directory. Directory must be in static folder of django project.
    Cycles through directory and extracts individual names and paths. Passes individual names to function syllables to count the
    number of syllables in word. Inserts names, paths, number of syllables, and an id into pre-made word table
    in database. Strips names of any non-alpha character and does not allow names with whitespace or duplicate names.
    Returns None
    '''
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
            new = unicodedata.normalize('NFKC', new)
            executestring += "({},'{}', NULL, {}, NULL, NULL, NULL),".format(word_id, new, num_syllables)
            word_id +=1
    executestring = executestring[0:-1]
    cursor.execute(executestring)
    db.commit()
    return
"""

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
            new = unicodedata.normalize('NFKC', new)
            executestring = "INSERT INTO alphabet VALUES ('{}','','{}')".format(new, finalpath)
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
        executestring = "UPDATE alphabet SET vowel = 'vowel' where letter like '%{}%'".format(v)
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

    executestring = "UPDATE alphabet SET vowel = 'semivowel' where letter = 'y' or letter = 'w'"
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

    executestring = "UPDATE alphabet SET vowel = 'consonant' where vowel = ''"
    cursor.execute(executestring)

    db.commit()
    return

def cycleGramCodes(directory_in_str):
    directory = directory_in_str
    with open(os.path.join(directory,GRAMCODE_FILENAME), 'r') as doc:
        lines = doc.readlines()

    for l in lines:
        #strip code to remove '\n'
        stripped_code = l.strip()
        executestring = "INSERT INTO gram_code VALUES ('{}')".format(stripped_code)
        cursor.execute(executestring)
    db.commit()

def cycleLemma(directory_in_str):
    directory = directory_in_str
    with open(os.path.join(directory,LEMMA_FILENAME), 'r') as doc:
        lines = doc.readlines()

    lemma_id = 0
    lemma_dict = {}

    #TODO add part_of_speech stuff
    #TODO add animate stuff
    #TODO add trransitive stuff
    #TODO add translation stuff

    for l in lines:
        content = unicodedata.normalize('NFKC', l)

        #strip code to remove '\n'
        stripped_code = content.strip()

        executestring = "INSERT INTO lemma VALUES ('{}', '{}', NULL, NULL,NULL,NULL,NULL,NULL)".format(
                        lemma_id,
                        stripped_code,
                        )
        #print(executestring + '\n')
        lemma_dict[stripped_code] = lemma_id
        cursor.execute(executestring)
        lemma_id += 1

    return lemma_dict


def main():

    dbInfo()
#I got upset at having to type the same stuff in again and again. -Brent
    """
    word = input("Please enter the path to 'word' recordings: ")
    print("\n")
    alphabet = input("Please enter the path to 'alphabet' recordings: ")
    print("\n")
    sound = input("Please enter the path to 'letter pair' recordings: ")
    """
    word = settings.PATH_TO_WORD
    alphabet = settings.PATH_TO_ALPHABET
    sound = settings.PATH_TO_LETTERPAIR
    #path to ../Linguistics/
    linguistics = os.path.abspath(os.path.join(os.path.dirname(sys.path[0]),'Linguistics'))

    cycleGramCodes(linguistics)


    #cycle lemmas and obtain a list of added lemmas for cycleWords to use
    lemma_dict = cycleLemma(linguistics)

    cycleWords(linguistics, lemma_dict)
    cycleLetters(alphabet)
    cycleSound(sound)


    db.commit()
    db.close()

    return


main()
