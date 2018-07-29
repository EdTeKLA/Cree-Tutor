# -*- coding:utf-8 -*-

"""
Created on Wed Jul 04 2018

This is a script that analyzes words.txt and creates two files.
1. a list of lemmas called lemmas.txt
2. a list of gram_codes called gram_codes.txt

This system will need to be replaced by a better system.
Please don't add new words to words.txt
"""

import os
import subprocess

ANALYZE_COMMAND = ['lookup', '-q', '-flags', 'mbTTx', '/home/brent/main/langs/crk/src/analyser-gt-norm.xfst']
FILENAME = "words.txt"
LEMMA_FILENAME = "lemmas.txt"
GRAM_CODE_FILENAME = "gram_codes.txt"
FAIL_FILENAME = "failures.txt"

def loadFile(FILENAME):
    """
    arguments: FILENAME is defined at the beginning of script.

    returns: a list of all the words
    """

    with open(FILENAME, 'r') as file:
        lines = file.readlines()

    return lines

def createFiles(words):
    """
    arguments: words is a list of words created by loadFile.

    createFiles queries the fst for each item in the list past to it.
    If the fst has an analysis, the lemma and gram_code of the analysis are remembered
    If the fst fails an analysis it is stored as a failure.
    The final lists of failures, lemmas and gram_codes are saved as separate files.
    """
    lemmas = []
    gram_codes = []
    fails = []

    for w in words[:1]:
        print(w.strip())
        PIPE = subprocess.PIPE
        proc = subprocess.Popen(ANALYZE_COMMAND, stdin=PIPE, stderr=PIPE, stdout=PIPE)
        kwargs = {'input':w.strip()}
        output, err = proc.communicate(input=w, timeout=3)
        print(output)
        print(err)


def main():

    words = loadFile(FILENAME)
    createFiles(words)

main()
