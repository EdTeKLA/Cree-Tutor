"""
The final product of this script should be the creation of a file which
can be used to import words into the database.

"""
import os
import sys
import unicodedata

def get_file_dict():
    """
    returns a dictionary which contains words as keys and the filenames as values.
    """
    file_dict = {}

    with open("/home/brent/Repositories/CreeTutor/Linguistics/words_complete.txt", 'r') as filenames:
        file_lines = filenames.readlines()
    for e in file_lines:
        #interpret text and fiddle with it to get the data
        content = unicodedata.normalize("NFC", e)
        content_as_list = content.split('\t')
        #sys.stdout.write(str(content_as_list) + '\n')
        word = content_as_list[0]
        filenames_as_list = content_as_list[1].strip().split(',')
        #sys.stdout.write(word + ' ' + str(filenames_as_list) + '\n')

        file_dict[word] = filenames_as_list


    return file_dict

def create_file(file_dict):
    """
    returns nothing

    will create a file names words_for_db.txt
    """
    with open("/home/brent/Repositories/CreeTutor/Linguistics/words_fst.txt", 'r') as fst:
        fst_lines = fst.readlines()
        #a little formatting
        #acimosis	atim+N+AN+Der/Dim+N+AN+Sg
        #becomes
        # ['acimosis', 'atim', 'N+AN+Der/Dim+N+AN+Sg']

    lemmas_and_gram_codes = []

    for e in fst_lines:
        #get all the components
        content = unicodedata.normalize('NFC', e)
        line_as_list = content.strip().split('\t')
        word = line_as_list[0]
        fst_output = line_as_list[1]
        lemma = fst_output.split('+')[0]

        #work on gram_code. split on +, remove preverbs, join on +
        gram_code = fst_output.split("+")
        sys.stdout.write(str(gram_code) + '\n')
        if len(gram_code) > 0:
            sys.stdout.write(str(gram_code) +' contains a + \n')
            while 'PV' in gram_code[0]:
                gram_code = gram_code[1:]
            if 'RdplW' in gram_code[0]:
                gram_code = gram_code[1:]
            lemma = gram_code[0]
            gram_code = gram_code[1:]
        gram_code = '+'.join(gram_code)
        files = ','.join(file_dict[word])
        #debugging line
        #sys.stdout.write(str(type(gram_code)) + '\n')

        lemmas_and_gram_codes.append(
                                    word +'\t'+
                                    gram_code +'\t'+
                                    'NULL' +'\t'+
                                    lemma +'\t'+
                                    files +'\t'+
                                    '\n'
                                    )

    with open("/home/brent/Repositories/CreeTutor/Linguistics/words_for_db.txt", 'w') as doc:
        #write it all to a file
        for e in lemmas_and_gram_codes:
            doc.write(e)

def main():
    #open words_complete and create a dictionary of words to filenames
    file_dict = get_file_dict()

    #open words_fst and cycle through each word.
        #should look like this:
        #atim	N+AN+Sg	dog	atim	atim.wav
        #word   gram    trans   lemma   filename.wav,filename.mp4
        #However, translation will need to be added by hand...yay,
        #"Looking forward to that!!!"
    create_file(file_dict)



main()
