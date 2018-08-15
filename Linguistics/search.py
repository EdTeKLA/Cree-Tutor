
import unicodedata
import os
import sys

DICT_FILENAME = "C:\\Users\\Brent\\Repositories\\ExtrasForCreeTutor\\scrubbed2.txt"
LEMMA_FILEPATH = os.path.abspath(os.path.join(os.path.dirname(sys.path[0]),'Linguistics'))
LEMMA_FILENAME = "lemmas.txt"
NEW_LEMMA_FILENAME = 'lemmas_REMOVE_OR_REPLACE.txt'

def search_dict(lemma, dictionary):
    #Query the dictionary and return the result or NULL
    if lemma in dictionary:
        return dictionary[lemma]
    else:
        return "NULL"

def main():

    #get the dictionary
    with open(DICT_FILENAME, 'r', encoding='utf-8') as dict_doc:
        dict_lines = dict_doc.readlines()
    #put the dictionary into a dictionary object
    dict = {}
    for e in dict_lines:
        normalized = unicodedata.normalize("NFC", e)
        #get rid of the new lines and split on tilda
        split = normalized.strip().split('~')
        #keys are the first column, values are the fifth
        if dict.get(split[0]) == None:
            dict[split[0]] = split[4]



    # print(list(dict.items())[:100])

    #get lemma.txt
    with open(os.path.abspath(os.path.join(LEMMA_FILEPATH, LEMMA_FILENAME)), 'r', encoding='utf-8') as lemma_doc:
        lemma_lines = lemma_doc.readlines()

    list_of_lemmas = []

    #for each lemma, search the dictionary and return the translation
    # store this translation in a list of tuples
    for lemma in lemma_lines:
        normalized = unicodedata.normalize('NFC', lemma)
        stripped = normalized.strip()
        translation = search_dict(stripped, dict)
        list_of_lemmas.append([stripped, translation])

    print(list_of_lemmas)

    #write the list of tuples to a text file
    with open (NEW_LEMMA_FILENAME, 'w', encoding='utf-8') as write_doc:
        for e in list_of_lemmas:
            write_doc.write(e[0] + '~' + e[1] + '\n')

main()
