# -*- coding:utf-8 -*-

"""
Created on Wed Jul 05 2018
by Brent

Reads words_fst_output.txt and creates a few files.

Here is the sequence of things to do to make this work.
OR just do this the right way when you find out how.

run this stuff from the command line e.i. "python create_lemma_txt.py"
each time you run it you edit the file.
Again, I realize how stupid this is.
If you find this, let me know how to fix it -Brent, bpancheshen@gmail.com
1. create lemmas.txt using create_lemma()
2. create gram_codes.txt using create_gram_codes()
3. !!!!!!DELETE PIWAN!!!!! Because its so dumb!
4. Sort gram_codes using sort_gram_codes()

"""

#create_lemma()
#create_gram_codes()
#sort_gram_codes()

def create_lemma():
    with open(r'/home/brent/Repositories/CreeTutor/Linguistics/words_fst_output.txt','r') as f:
        lines = f.readlines()
    lemmas = []

    #For every line in words_fst_output.txt,
    for l in lines:
        #if the line isn't blank,
        if l.strip() != "":
            #get the lemma,
            lemma = l.split()[0]
            with open('lemmas.txt', 'a') as file:
                if lemma not in lemmas:
                    lemmas.append(lemma)
                    #then, write the lemma to the file if it isn't already there.
                    file.write(lemma + '\n')


def create_gram_codes():
    with open(r'/home/brent/Repositories/CreeTutor/Linguistics/words_fst_output.txt','r') as f:
        lines = f.readlines()
    gram_codes = []

    #For each line in words_fst_output.txt
    for l in lines:
        #if the line isn't blank and it isn't an fst failure,
        if l.strip() != "" and '+?' not in l:
            #get atim+N+AN+Sg
            l = l.split()[1]
            #split it
            l = l.split('+')
            #remove PV and other front ornaments
            while 'PV' in l[0]:
                l = l[1:]
            if 'RdplW' in l[0]:
                l = l[1:]
            l=l[1:]
            #bring it back together
            gram_code = '+'.join(l)

            with open('gram_codes.txt', 'a') as file:
                if gram_code not in gram_codes:
                    gram_codes.append(gram_code)
                    #then, write the lemma to the file if it isn't already there.
                    file.write(gram_code + '\n')

#THIS FAILS ON PIWAN. MAKE SURE YOU JUST MANUALLY DELETE THIS!


def sort_gram_codes():
    with open('gram_codes.txt', 'r') as file:
        lines = file.readlines()
    sorted_lines = sorted(lines)
    with open('sorted_gram_codes.txt', 'w+') as save_file:
        save_file.write(''.join(sorted_lines))
