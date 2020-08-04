import os
import sys
import unicodedata
from cree_sro_syllabics import sro2syllabics

# filename
WORDS_FILENAME = 'words_for_db.txt'

# get the Cree SRO words from the word text file
direct = linguistics = os.path.abspath(os.path.join(os.path.dirname(sys.path[0]),'Linguistics'))

with open(os.path.join(direct, WORDS_FILENAME), 'r', encoding='utf-8') as readfile:
    word_lines = readfile.readlines()

# open text file
syllabics_file = open('syllabics.txt','w')

# list of syllabics characters
characters = {
    "ê": "ᐁ",
    "i": "ᐃ",
    "î": "ᐄ",
    "o": "ᐅ",
    "ô": "ᐆ",
    "a": "ᐊ",
    "â": "ᐋ",
    "wê": "ᐍ",
    "wi": "ᐏ",
    "wî": "ᐑ",
    "wo": "ᐓ",
    "wô": "ᐕ",
    "wa": "ᐘ",
    "wâ": "ᐚ",
    "w": "ᐤ",
    "p": "ᑊ",
    "pê": "ᐯ",
    "pi": "ᐱ",
    "pî": "ᐲ",
    "po": "ᐳ",
    "pô": "ᐴ",
    "pa": "ᐸ",
    "pâ": "ᐹ",
    "pwê": "ᐻ",
    "pwi": "ᐽ",
    "pwî": "ᐿ",
    "pwo": "ᑁ",
    "pwô": "ᑃ",
    "pwa": "ᑅ",
    "pwâ": "ᑇ",
    "t": "ᐟ",
    "tê": "ᑌ",
    "ti": "ᑎ",
    "tî": "ᑏ",
    "to": "ᑐ",
    "tô": "ᑑ",
    "ta": "ᑕ",
    "tâ": "ᑖ",
    "twê": "ᑘ",
    "twi": "ᑚ",
    "twî": "ᑜ",
    "two": "ᑞ",
    "twô": "ᑠ",
    "twa": "ᑢ",
    "twâ": "ᑤ",
    "k": "ᐠ",
    "kê": "ᑫ",
    "ki": "ᑭ",
    "kî": "ᑮ",
    "ko": "ᑯ",
    "kô": "ᑰ",
    "ka": "ᑲ",
    "kâ": "ᑳ",
    "kwê": "ᑵ",
    "kwi": "ᑷ",
    "kwî": "ᑹ",
    "kwo": "ᑻ",
    "kwô": "ᑽ",
    "kwa": "ᑿ",
    "kwâ": "ᒁ",
    "c": "ᐨ",
    "cê": "ᒉ",
    "ci": "ᒋ",
    "cî": "ᒌ",
    "co": "ᒍ",
    "cô": "ᒎ",
    "ca": "ᒐ",
    "câ": "ᒑ",
    "cwê": "ᒓ",
    "cwi": "ᒕ",
    "cwî": "ᒗ",
    "cwo": "ᒙ",
    "cwô": "ᒛ",
    "cwa": "ᒝ",
    "cwâ": "ᒟ",
    "m": "ᒼ",
    "mê": "ᒣ",
    "mi": "ᒥ",
    "mî": "ᒦ",
    "mo": "ᒧ",
    "mô": "ᒨ",
    "ma": "ᒪ",
    "mâ": "ᒫ",
    "mwê": "ᒭ",
    "mwi": "ᒯ",
    "mwî": "ᒱ",
    "mwo": "ᒳ",
    "mwô": "ᒵ",
    "mwa": "ᒷ",
    "mwâ": "ᒹ",
    "n": "ᐣ",
    "nê": "ᓀ",
    "ni": "ᓂ",
    "nî": "ᓃ",
    "no": "ᓄ",
    "nô": "ᓅ",
    "na": "ᓇ",
    "nâ": "ᓈ",
    "nwê": "ᓊ",
    "nwa": "ᓌ",
    "nwâ": "ᓎ",
    "s": "ᐢ",
    "sê": "ᓭ",
    "si": "ᓯ",
    "sî": "ᓰ",
    "so": "ᓱ",
    "sô": "ᓲ",
    "sa": "ᓴ",
    "sâ": "ᓵ",
    "swê": "ᓷ",
    "swi": "ᓹ",
    "swî": "ᓻ",
    "swo": "ᓽ",
    "swô": "ᓿ",
    "swa": "ᔁ",
    "swâ": "ᔃ",
    "y": "ᐩ",
    "yê": "ᔦ",
    "yi": "ᔨ",
    "yî": "ᔩ",
    "yo": "ᔪ",
    "yô": "ᔫ",
    "ya": "ᔭ",
    "yâ": "ᔮ",
    "ywê": "ᔰ",
    "ywi": "ᔲ",
    "ywî": "ᔴ",
    "ywo": "ᔶ",
    "ywô": "ᔸ",
    "ywa": "ᔺ",
    "ywâ": "ᔼ",
    "th": "ᖮ",
    "thê": "ᖧ",
    "thi": "ᖨ",
    "thî": "ᖩ",
    "tho": "ᖪ",
    "thô": "ᖫ",
    "tha": "ᖬ",
    "thâ": "ᖭ",
    "l": "ᓬ",
    "r": "ᕒ",
    "h": "ᐦ",
    "hk": "ᕽ",
}

values = characters.values()
print(values)

for e in word_lines:
    #No double characters! No other funny business!
    content = unicodedata.normalize("NFC", e)
    #Split the columns into a list
    content_as_list = content.split('\t')

    if len(content_as_list) != 5:
        sys.stdout.write(
                                "Error on line " + str(word_id) + '\n' +
                                str(content_as_list) + '\n'
                                )
        break
    else:
        #get the stuff, man
        word = content_as_list[0]
        syllabics = sro2syllabics(word)
        # 'apsis' did not get converted
        if syllabics == 'apsis':
            syllabics = 'ᐊᑊᓯᐢ'
        
        # if it doesn't get converted, set as NULL
        for i in syllabics:
            if i not in values:
                syllabics = 'NULL'

        syllabics_file.write(syllabics + '\n')

syllabics_file.close()

