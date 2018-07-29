"""
This script creates a txt file which contains all of the words in statis/sound/words/
and tries it's best to match up the word with the filename.
"""

import os
import sys
import re
import unicodedata

DIRECTORY =  "/home/brent/Repositories/CreeTutor/CreeTutorBackEnd/lettergame/static/lettergame/sound/Words"
#Open words and get all the words
with open('/home/brent/Repositories/CreeTutor/Linguistics/words_e.txt', 'r') as words:
    words_list = words.readlines()
    for i in range(len(words_list)):
        words_list[i] = unicodedata.normalize('NFC', words_list[i])

#Open sentences.txt and get all the sentences
with open('/home/brent/Repositories/CreeTutor/Linguistics/sentences.txt', 'r') as sents:
    sents_list = sents.readlines()

#create a dictionary
words_dict = {}



with open("/home/brent/Repositories/CreeTutor/Linguistics/words_complete.txt",'w') as doc:
    #get a sorted list of filenames
    files = []
    for filename in os.listdir(DIRECTORY):
        files.append(unicodedata.normalize('NFC', filename))
    files.sort()
    event = 1
    for word in words_list:
        comp = re.compile(word.strip())
        word = unicodedata.normalize('NFC', word).strip()
        for f in files:
            string = f.split('.')[0].split('-')[0].split('_')[0]
            if event ==0:
                sys.stdout.write(string + '\n')
                for i in string:
                    sys.stdout.write(str(ord(i))+'\n')
                sys.stdout.write(word + '\n')
                for i in word:
                    sys.stdout.write(str(ord(i))+'\n')
            event =+1
            if re.fullmatch(comp,string)!=None:
                if word in words_dict.keys():
                    words_dict[word].append(f)
                else:
                    words_dict[word] = [f]
        if word in words_dict.keys():
            doc.write(re.sub('e','ê',word) + '\t' + ",".join(words_dict[word]) + "\n")
        else:
            doc.write(re.sub('e','ê',word) + '\n')
