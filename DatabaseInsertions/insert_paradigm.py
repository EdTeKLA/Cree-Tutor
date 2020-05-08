# look up "read file python"
#string to list: look up "python split function"

import abc
import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'CreeTutorBackEnd'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
import django
django.setup()

from lettergame.models import *
from CreeTutorBackEnd import settings_secret

cursor = None
db = None

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
    models = [
        recipe
    ]
    # All the models that will be wiped out

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
    paradigm = "ai.txt"

    # Setting the folders for the static content of letter game
    # words_directory = settings_secret.PATH_TO_WORD
    # letters_directory = settings_secret.PATH_TO_ALPHABET
    # pairs_directory = settings_secret.PATH_TO_LETTERPAIR
    # The models that need to be fixed.

    @staticmethod
    def insert_into_db():
        LetterGameInsertions.__cycle_paradigms()

    @staticmethod
    def __cycle_paradigms():
        f = open("ai.txt", "r")
        for line in f:
            line = line.split(",")
            prefix = line[0].strip()
            suffix = line[1].strip()
            independent_or_conjunct = line[2].strip()
            special_rule = line[3].strip()
            joiner = line[4].strip()
            pronoun = line[5].strip()
            paradigm = line[5].strip()
            if len(line) == 6:
                e = "INSERT INTO ai(prefix, suffix, independent_or_conjunct, special_rule, joiner, pronoun, paradigm) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                    prefix, suffix, independent_or_conjunct, special_rule, joiner, pronoun, paradigm)
                cursor.execute(e)
        db.commit()

        return
        # open file and cycle through it line by line
        # separate by comma
        # insert into model