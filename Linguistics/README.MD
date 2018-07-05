# Linguistics

## Using fst from terminal


Create words_fst_output.txt
* cat words.txt | lookup -q -flags mbTT ~/main/langs/crk/src/analyser-gt-desc.xfst > words_fst_output.txt


Create failures.txt
* cat words_fst_output.txt | grep +? > failures.txt
