"""
Files stores the function that add all the configurations to the database. It can also be used to update the
configuration because of the types of queries/functions it uses.
"""

import sys

import django
import os

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
django.setup()
from transcription.models import *

def add_configs_to_db():
    """
    Read the file description on line 1.
    :return:
    """
    # Creating the configs
    configs = {
        'SLIDING_WINDOW_SIZE_FOR_FETCH': 5,
        'MIN_NUMBER_OF_CHOICES': 3,
        'CHANGE_SCORE_BY': 50,
        'SCORE_SCALAR_MIN': 0.2,
        'TRANSCRIPTION_RATE_TO_INCREASE_SCORE': 0.80,
        'TRANSCRIPTION_RATE_TO_DECREASE_SCORE': 0.40,
    }

    # Going through the configs and add to db
    for key, value in configs.items():
        TranscriptionConfig.objects.get_or_create(name=key, config=value)

if __name__ == '__main__':
    add_configs_to_db()