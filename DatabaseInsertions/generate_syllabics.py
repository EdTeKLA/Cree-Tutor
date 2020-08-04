from getpass import getpass
import os
import sys
import re
import unicodedata
from cree_sro_syllabics import sro2syllabics

def addSyllabics(base_path, filename, seperator='\t'):
    # set up the file to be read and file to be created
    f_in = open(os.path.join(base_path, filename), mode='r')
    f_out = open(os.path.join(base_path, filename[:-4]+'_wsyllabics.txt'), mode='w')
    # read each line and append syllabics
    for line in f_in:
        # take out the line break
        line = re.sub(r'\n','',line)
        # split the line into an array so that we can access sro individually
        line = line.split(seperator)
        # get syllabics from sro
        syl = sro2syllabics(line[0])
        line.append(syl)
        # join and format syllabics into line
        line = seperator.join(line)
        line += '\n'
        # write it out
        f_out.write(line)
    # close the files
    f_in.close()
    f_out.close()


def main():
    #path to ../Linguistics/
    linguistics = os.path.abspath(os.path.join(os.path.dirname(sys.path[0]),'Linguistics'))
    # Files to append info to
    lemma_file = 'lemmas.txt'
    words_file = 'words_for_db.txt'
    try:
        # add syllabics to lemma table
        addSyllabics(linguistics, lemma_file,seperator='~')
        # add syllabics to word table
        addSyllabics(linguistics, words_file)
    except Exception as e:
        for err in e.args:
            print(err)
    else:
        print('Syllabics successfully added to words_for_db.txt and lemmas.txt!')

if __name__ == "__main__":
    main()
    