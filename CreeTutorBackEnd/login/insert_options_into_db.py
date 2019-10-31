import sys
import django
import os
import json
import pprint as pp

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
django.setup()

from login.models import Gender, AgeLevels, LanguageLevels, LanguagesSpoken

def insert_genders_into_db():
    """
    Function to insert gender choices into the gender table
    """
    # The gender options
    gender_options = ['Female', 'Male', 'Non-Binary', 'Prefer not to say']

    for option in gender_options:
        Gender.objects.get_or_create(gender=option.lower())


def insert_ages_into_db():
    """
    Function to insert age ranges into the age range table
    """
    # The gender options
    age_range_options = ['12 or under', '12-18', '19-29',
                         '30-39', '40-49', '50-59', '60-69', '70 and up', 
                         'Prefer not to say']

    for option in age_range_options:
        AgeLevels.objects.get_or_create(age_range=option.lower())

def insert_languages_into_db():
        # load the json file with a list of all languages
        with open('./static/login/js/languages.json') as json_file:
                language_option = json.load(json_file)
        
        for option in language_option.get('languages'):
                LanguagesSpoken.objects.get_or_create(language=option.lower())

def insert_language_levels_into_db():
    """
    Function to insert age ranges into the age range table
    """
    # The gender options
    language_level_options = ['Primary', 
                              'Fluent, no communication problems',
                              'Lots of experience, not quite fluent but can communicate well in the language', 
                              'Some experience, can hold basic, casual conversations', 
                              'Little experience, can use and understand basic sentences and questions'
                              ]

    for option in language_level_options:
        LanguageLevels.objects.get_or_create(language_level=option.lower())

if __name__ == '__main__':
        insert_languages_into_db()
        insert_genders_into_db()
        insert_ages_into_db()
        insert_language_levels_into_db()
