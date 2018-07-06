# Linguistics

## Using fst from terminal


Create words_fst_output.txt
* cat words.txt | lookup -q -flags mbTT ~/main/langs/crk/src/analyser-gt-desc.xfst > words_fst_output.txt


Create failures.txt
* cat words_fst_output.txt | grep +? > failures.txt

## How do deal with Cree Syllables

1. Any group of CV is a syllable for sure.
* o(ki)s(ki)n(wa)(mâ)(kê)w
2. Vowels on their own are also Syllables
* (o)(ki)s(ki)n(wa)(mâ)(kê)w
3. Word final consonants will be the coda of the last syllable.
* (o)(ki)s(ki)n(wa)(mâ)(kêw)
4. If the C in a CV syllable is a /w/, then it can be a C(w)V syllable.
* (o)(ki)s(ki)(nwa)(mâ)(kêw)
5. Everything else is a coda
* (o)(kis)(ki)(nwa)(mâ)(kêw)

Brent, What's a coda?
* A coda is everything after the vowel in the syllable. The coda of 'strict' is /kt/.

If a linguist needs this to be defended, it's probably a trap. Look out for universal grammar proponents. These rules are designed to mirror Cree syllabics.
