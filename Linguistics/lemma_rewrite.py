import os
import sys

with open("C:\\Users\\Brent\\Repositories\\CreeTutor\\Linguistics\\words_for_db.txt", 'r') as doc:
    words = doc.readlines()

lemmas = []
gram_codes = []

for line in words:
    lemma = line.split('\t')[3]
    gram_code = line.split('\t')[1]

    if lemma not in lemmas:
        lemmas.append(lemma)

    if gram_code not in gram_codes:
        gram_codes.append(gram_code)

with open(".\\Linguistics\\lemmas.txt", 'w') as lemma_file:
    for l in lemmas:
        lemma_file.write(l + '\n')

with open(".\\Linguistics\\gram_codes.txt", 'w') as gram_code_file:
    for l in gram_codes:
        gram_code_file.write(l + '\n')
