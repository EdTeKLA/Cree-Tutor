"""
File contains all the classes/methods/functions needed to insert data into the following tables:
    - letter_pair
    - alphabet
    - word
    - gram_code
"""

# Setup to use the django orm
import unicodedata

import abc
import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'CreeTutorBackEnd'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
import django
django.setup()

from lettergame.models import *
from CreeTutorBackEnd import settings_secret
from LanguageHelpers import *


class InsertIntoDB(abc.ABC):
    """
    Class was created so that it can be subclassed by other classes that add objects to db and to make sure they have
    a template to follow
    """

    @staticmethod
    @abc.abstractmethod
    def insert_into_db():
        pass


class DeleteData:
    """
    Class was created to hold methods that will delete data from a given model or all models defined in the list below.
    """
    # All the models that will be wiped out
    models = [
        # WordDistractors,
        Word,
        GramCode,

        DLSDistractedBy,
        DLSDistractors,
        PairDistractor,
        PairUserSeen,
        LetterPair,

        SLSDistractedBy,
        SLSDistractors,
        LetterDistractor,
        LetterUserSeen,

        LetterDistractor,
        Alphabet,

        DistractorType,
        # MinimalPair,

        Creedictionarydotcom,
        recipe
    ]

    @staticmethod
    def empty_all_models():
        """
        Delete all the data in the models
        """
        # Iterate through LetterGameInsertions the models and call the empty model method to clean them out
        for model in DeleteData.models:
            DeleteData.empty_model(model)

    @staticmethod
    def empty_model(model):
        """
        Delete all data from the model.
        """
        model.objects.all().delete()


class LetterGameInsertions(InsertIntoDB):
    """
    Class was created to clean out and insert data into the following tables:
        - letter_pair
        - alphabet
        - word
        - gram_code
    """

    # Setting the file names, stays constant across all the instances
    gramcode_filename = 'gram_codes.txt'
    lemma_filename = 'lemmas.txt'
    words_filename = 'words_for_db.txt'
    linguistic_directory = os.path.abspath(os.path.join(os.path.dirname(sys.path[0]), 'Linguistics'))
    # Setting the folders for the static content of letter game
    words_directory = settings_secret.PATH_TO_WORD
    letters_directory = settings_secret.PATH_TO_ALPHABET
    pairs_directory = settings_secret.PATH_TO_LETTERPAIR
    # The models that need to be fixed.

    @staticmethod
    def insert_into_db():
        """
        Method was created to call all the methods in order to make the class word properly.
        """
        # Insert the gram codes
        # LetterGameInsertions.__cycle_gram_codes()
        # # Insert the words
        # LetterGameInsertions.__add_words_to_db()
        # # Inserts the letters to the database
        # LetterGameInsertions.__add_alphabet_to_db()
        # # Inserts the letter pairs in the db
        # LetterGameInsertions.__add_letterpairs_to_db()
        LetterGameInsertions.__add_dictionary_to_db()
        LetterGameInsertions.__cycle_paradigms()

    @staticmethod
    def __cycle_gram_codes():
        """
        Method goes through the file defined in gramcode_filename and adds the contents to the database in the GramCode
        table.
        :return:
        """
        # Open the file and read all the lines
        gram_codes_lines = None
        with open(os.path.join(
                LetterGameInsertions.linguistic_directory,
                LetterGameInsertions.gramcode_filename), 'r', encoding='utf-8') as gram_codes_file:
            gram_codes_lines = gram_codes_file.readlines()

        # Clean up the gram code lines and create objects from them
        gram_code_line_objects = []
        for gram_codes_line in gram_codes_lines:
            # Clean the line
            gram_codes_line = gram_codes_line.strip()
            # Create an object
            gram_code_line_objects.append(GramCode(gram_code=gram_codes_line))

        # Add the gram codes to the db, ignore any duplicates if they have been inserted before
        GramCode.objects.bulk_create(gram_code_line_objects, ignore_conflicts=True)

    @staticmethod
    def __add_words_to_db():
        """
        Gets a path to the words directory, goes thorugh the directory to extract names and paths. Counts the number of
        syllables in the word. Inserts the names, paths, number of syllables into the Word table. Removes white-space/
        non-alpha chars and duplicates.
        :return:
        """
        # Add the words that need to be added to db to this list
        word_objects = []

        # Open the file and get it ready for reading
        file = open(os.path.join(LetterGameInsertions.linguistic_directory
                                 , LetterGameInsertions.words_filename), 'r', encoding='utf-8')

        # Read the file line by line and process
        for line in file:
            # No double characters! No other funny business!
            content = unicodedata.normalize("NFC", line)
            # Split the line at the tabs
            content_as_list = content.split('\t')
            # If there aren't enough columns, print which word caused the failure
            # One will need to go through words_for_db and find out why.
            if len(content_as_list) != 5:
                # Raise the exception to stop the execution
                raise Exception(" A line in the file does not have 5 components, line: " + str(line))
            else:
                # Get the gram code object
                gram_code, _ = GramCode.objects.get_or_create(gram_code=content_as_list[1])
                # Create an object from the line and add it to the list
                word_objects.append(
                    Word(
                        word=content_as_list[0],
                        gram_code=gram_code,
                        translation=content_as_list[2],
                        num_syllables=LanguageHelpers.count_syllables(content_as_list[0])
                    )
                )

        file.close()

        # Add all the words into the words table
        Word.objects.bulk_create(word_objects, ignore_conflicts=True)

    @staticmethod
    def __add_alphabet_to_db():
        """
        Goes through the alphabet directory, gets all the files in the directory, adds the value of vowel and bulk
        inserts into the database.
        :return:
        """
        # The objects that will be passed into bulk create
        alphabet_objects = []
        # Get file names and path from the records directory
        letters = LetterGameInsertions.__get_files_from_directory(LetterGameInsertions.letters_directory)
        # Now go through every letter and create an object from it and check to see what type of letter it is
        for letter in letters:
            alphabet_objects.append(
                Alphabet(
                    letter=letter['characters'],
                    sound=letter['path'],
                    vowel=LanguageHelpers.type_of_letter(letter['characters'])
                )
            )
            letter = models.CharField(primary_key=True, max_length=2)
            vowel = models.TextField(blank=True, null=True)
            sound = models.TextField(blank=True, null=True)

        # Add to db
        Alphabet.objects.bulk_create(alphabet_objects, ignore_conflicts=True)

    @staticmethod
    def __add_letterpairs_to_db():
        """
        Goes through the alphabet directory, gets all the files in the directory, adds the value of vowel and bulk
        inserts into the database.
        :return:
        """
        # The objects that will be passed into bulk create
        letterpair_objects = []
        # Get file names and path from the records directory
        pairs = LetterGameInsertions.__get_files_from_directory(LetterGameInsertions.pairs_directory)
        # Go through every pair, get extra info and add to db
        for pair in pairs:
            # Break the pair up
            first, second = LanguageHelpers.split_pair_into_letters(pair['characters'])
            # Create the object
            letterpair_objects.append(
                LetterPair(
                    pair=pair['characters'],
                    sound=pair['path'],
                    first_letter_id=first,
                    second_letter_id=second
                )
            )


        LetterPair.objects.bulk_create(letterpair_objects, ignore_conflicts=True)

    @staticmethod
    def __get_files_from_directory(directory):
        """
        Goes through the directory passed in and read all the file names, parses/cleans them and returns a list of
        dictionaries with the path to the file and the characters that should be attached to the file.
        :param directory:
        :return:
        """
        # Records list
        records = []
        # Encode the path to the directory according to the os
        directory_cleaned = os.fsencode(directory)
        # Now get all the files in the directory and go through it one by one
        for file in os.listdir(directory_cleaned):
            # Decode the filename passed found in the directory
            file_cleaned = os.fsdecode(file)
            # Hardcoded to only .wav and m4a files
            if file_cleaned.endswith(".wav") or file_cleaned.endswith(".m4a"):
                path_name = os.path.join(directory, file_cleaned)
                final_path = os.fsdecode(path_name)
                # Change the backwards path to forwards cause Windows
                final_path = final_path.replace("\\", "/")
                # Remove the path up to static/ so that django can read the audio file without problems
                final_path = final_path.split('static/')[1]
                # Clean the file name, remove the extension, use the first part of the word as a title
                file_cleaned = file_cleaned.replace('.wav', '')
                file_cleaned = file_cleaned.replace('.m4a', '')
                if "._" in file_cleaned:
                    continue
                # Normalize
                file_cleaned = unicodedata.normalize('NFC', file_cleaned)
                # Create the dict and add to the list
                records.append({
                    'path': final_path,
                    'characters': file_cleaned
                })

        # Return the records
        return records

    @staticmethod
    def __add_dictionary_to_db():
        # The objects that will be passed into bulk create
        dict_objects = []
        entries=[]
        # Get file names and path from the records directory
        f = open("creedictionarydotcom.txt", 'r',encoding="utf-8")
        for line in f:
            # print(line)
            line = line.replace("\n", '')
            spe = line.split("~")
            if len(spe) == 1:
                continue
            p = dict()
            for i in range(len(spe)):
                a = spe[i].replace("-", "")
                a = a.replace('îy', 'iy')
                a = a.replace('ê', 'e')
                p[i] = a
            entries.append(p)

        # Now go through every letter and create an object from it and check to see what type of letter it is

        for p in entries:
            # s= "{}, {}, {}, {}, {}, {}".format(p[0], p[1], p[2], p[3], p[4], p[5])
            # print(s)
            # print()
            dict_objects.append(
                Creedictionarydotcom(
                    word = p[0],
                    plural = p[1],
                    syllabics = p[2],
                    pos = p[3],
                    translation = p[4],
                    dictionary = p[5]
                )
            )
        # Add to db
        Creedictionarydotcom.objects.bulk_create(dict_objects, ignore_conflicts=True)

        return

    @staticmethod
    def __cycle_paradigms():
        f = open("ai.txt", "r", encoding="utf-8")
        paradigms = []
        for line in f:
            line = line.split(",")
            prefix = line[0].strip()
            suffix = line[1].strip()
            independent_or_conjunct = line[2].strip()
            special_rule = line[3].strip()
            joiner = line[4].strip()
            pronoun = line[5].strip()
            paradigm = line[6].strip()
            translation = line[7].strip()
            print(line)
            paradigms.append(
                recipe(
                    prefix=prefix,
                    suffix=suffix,
                    independent_or_conjunct=independent_or_conjunct,
                    special_rule=special_rule,
                    joiner=joiner,
                    pronoun=pronoun,
                    paradigm=paradigm,
                    translation=translation

                )
            )
            recipe.objects.bulk_create(paradigms, ignore_conflicts=True)



        return


class LetterGameDistractorInsertions(InsertIntoDB):
    """
    Class was created to delete all the old distractors and insert new distractors listed in distractor files.
    """

    @staticmethod
    def insert_into_db():
        """
        Method was created to call all the methods in order to make the class word properly.
        """
        # Add all the distractor types to the db
        LetterGameDistractorInsertions.__add_distractor_type_to_db()
        # Now add the distractors to the db that are written to a file
        LetterGameDistractorInsertions.__add_letter_distactors_to_db()
        LetterGameDistractorInsertions.__add_letterpair_distractors_to_db()
        # Generate the distractors for words
        LetterGameDistractorInsertions.__generate_distractors_for_words()

    @staticmethod
    def __add_distractor_type_to_db():
        """
        Get the content of the file that contains the distractor types and write to db in bulk.
        :return:
        """
        # Read all the records
        records = LetterGameDistractorInsertions.__read_distractor_files(
            'distractor_type.txt',
            ['type', 'distraction', 'insro']
        )

        objects = []
        # Now go through every record and create objects from it
        for record in records:
            objects.append(
                DistractorType(**record)
            )

        # Write to file
        DistractorType.objects.bulk_create(objects, ignore_conflicts=True)

    @staticmethod
    def __add_letter_distactors_to_db():
        """
        Get the content of the files that contains the letter distractors and write to db in bulk.
        :return:
        """
        # Read all the records
        records = LetterGameDistractorInsertions.__read_distractor_files(
            'letter_distractor.txt',
            ['letter_id', 'distractor', 'type_id']
        )

        objects = []
        # Now go through every record and create objects from it
        for record in records:
            # Create the object
            objects.append(
                LetterDistractor(**record)
            )

        # Write to file
        LetterDistractor.objects.bulk_create(objects, ignore_conflicts=True)

    @staticmethod
    def __add_letterpair_distractors_to_db():
        """
        Get the content of the file that contains letter pair distractors and write to the db in bulk.
        :return:
        """
        # Read all the records
        records = LetterGameDistractorInsertions.__read_distractor_files(
            'pair_distractor.txt',
            ['pair_id', 'distractor', 'type_id']
        )

        objects = []
        # Now go through every record and create objects from it
        for record in records:
            # Get objects for the foreign keys
            # Create the object
            objects.append(
                PairDistractor(**record)
            )

        # Write to file
        PairDistractor.objects.bulk_create(objects, ignore_conflicts=True)

    @staticmethod
    def __read_distractor_files(file_name, labels):
        """
        Reads a file and returns the lines after they have been converted to dicts. The labels are what the dict keys
        are called.
        :param file_name:
        :param labels:
        :return:
        """
        # List that will be returned
        line_dicts = []
        # Open the file
        file = open(file_name, 'r', encoding='utf-8')
        # Go through it line by line
        for line in file:
            # Clean up the line and split it on the colors
            line = line.strip()
            line_as_list = line.split(":")
            # Create a dict and append it to the list
            line_dicts.append(
                {
                    labels[0]: line_as_list[0],
                    labels[1]: line_as_list[1],
                    labels[2]: line_as_list[2]
                }
            )

        # Close file and return content
        file.close()
        return line_dicts

    @staticmethod
    def __generate_distractors_for_words():
        """
        Method creates distractors for words. They are generated, not read from a file.
        :return:
        """
        # Create a list of the objects to add to the db
        word_distractor_objects = []
        # Get words that do not end or start with k, but have k in the middle and has 1 or 2 syllables
        selected_words = Word.objects.\
            exclude(word__endswith='k').\
            exclude(word__startswith='k').\
            filter(word__contains='k').\
            filter(num_syllables__lte=2)

        # Go through all the words that were fetched, replace the k with g and add to the list of word object list
        word_distractor_objects += \
            LetterGameDistractorInsertions.__change_word_distractors_and_add_to_db(selected_words, 'k', 'g', 3)

        # Get words with a p in it
        selected_words = Word.objects.\
            filter(word__contains='p').\
            filter(num_syllables__lte=2)

        # Go through the words again and replace the p's with the b's
        word_distractor_objects += \
            LetterGameDistractorInsertions.__change_word_distractors_and_add_to_db(selected_words, 'p', 'b', 3)

        # Deal with t's
        selected_words = Word.objects.\
            filter(word__contains='t').\
            filter(num_syllables__lte=2)

        word_distractor_objects += \
            LetterGameDistractorInsertions.__change_word_distractors_and_add_to_db(selected_words, 't', 'd', 3)

        # Deal with the rest of the words, just add all words
        # Get all the words
        all_words = Word.objects.filter(num_syllables__lte=2)
        # Loop through both
        for org_word in all_words:
            for second_word in all_words:
                if org_word.word != second_word.word:
                    word_distractor_objects.append(
                        WordDistractors(
                            word=org_word.word,
                            distractor=second_word.word,
                            type_id=7
                        )
                    )

        # Add to db
        WordDistractors.objects.bulk_create(word_distractor_objects, ignore_conflicts=True)

    @staticmethod
    def __change_word_distractors_and_add_to_db(selected_words, to_replace, with_replace, type):
        """
        Run through the words passed in and add to the db. Also replaces the phrase passed in.
        :return:
        """
        word_distractor_objects = []

        # Go through the words again and replace the p's with the b's
        for selected_word in selected_words:
            word_distractor_objects.append(
                WordDistractors(
                    word=selected_word.word,
                    distractor=selected_word.word.replace(to_replace, with_replace),
                    type_id=type
                )
            )

        return word_distractor_objects


class LetterGameMinimalPairInsertions(InsertIntoDB):
    """
    Class was created to go through minimal/close-ish pair files and add them to the db.
    """
    @staticmethod
    def insert_into_db():
        """
        Method was created to call all other methods that will add records to the db.
        :return:
        """
        LetterGameMinimalPairInsertions.__add_minimal_pairs_to_db()

    @staticmethod
    def __add_minimal_pairs_to_db():
        """
        Goes through every word in the db, check if they differ by one or two letter. If they do, add them to db with a
        particular type. If difference == 1, then insert into min pair and into word distractor with type 1, if diff ==
        2 then, just add as a type 3 distractor.
        :return:
        """
        # The minimal pair objects that will be added to the db
        minimal_pair_objects = []
        word_distractor_objects = []
        # Get all the words from the db
        words = Word.objects.all()
        # Go through words, on loop inside another, ignore same words or if the difference between the two is larger
        # than 2. If the the difference is 1 or 2, add to db.
        # Outer words
        for word in words:
            # The min pair
            for min_pair in words:
                if word.word == min_pair.word:
                    # If the two words are the same, skip
                    continue
                # Get the diff
                diff = LanguageHelpers.difference_between_words(word.word, min_pair.word)
                # If only one diff, add as minimal pair
                if diff == 1:
                    # Add the minimal pair
                    minimal_pair_objects.append(
                        MinimalPair(
                            word=word.word,
                            minpair=min_pair.word,
                            num_syllables=word.num_syllables
                        )
                    )
                    # Add the distractors
                    word_distractor_objects.append(
                        WordDistractors(
                            word=word.word,
                            distractor=min_pair.word,
                            type_id=1
                        )
                    )
                elif diff == 2:
                    # Add to distractor table
                    word_distractor_objects.append(
                        WordDistractors(
                            word=word.word,
                            distractor=min_pair.word,
                            type_id=3
                        )
                    )

        # Now add the two list of objects into the db
        MinimalPair.objects.bulk_create(minimal_pair_objects, ignore_conflicts=True)
        WordDistractors.objects.bulk_create(word_distractor_objects, ignore_conflicts=True)


if __name__ == '__main__':
    # First clean the db
    DeleteData.empty_all_models()
    # Now add the data, this does not include distractors
    LetterGameInsertions.insert_into_db()
    # Now add the distractors
    # LetterGameDistractorInsertions.insert_into_db()
    # Now add the minimal pairs to the db
    # LetterGameMinimalPairInsertions.insert_into_db()