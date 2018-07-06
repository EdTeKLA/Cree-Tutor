from django.db import models

'''
HOW TO:
-Create a model with Django:
    https://docs.djangoproject.com/en/2.0/topics/db/models/
-Integrate a legacy database:
    https://docs.djangoproject.com/en/2.0/howto/legacy-databases/
-Three-step guide to making model changes:
    1. Change your models (in models.py)
    2. Run python manage.py makemigrations to create migrations for those changes
    3. Run python manage.py migrate to apply those changes to the database
    NOTE: If you change the name of model or field, PLEASE ENSURE that you change it everywhere else it
    could be changed e.g. in views.py
-Create a model(table) using mysql:
    1. Create table in mysql
    2. Run python manage.py inspectdb
    3. Find the Python Model script for your new model and copy it
    4. Paste it into this file.
    5. Make appropriate migrations and desired adjustments.
    NOTE: Not every table from the database needs to be in models, only if it is being used
    elsewhere, e.g. views.py
-Understanding migrations:
    https://docs.djangoproject.com/en/2.0/topics/migrations/
-Class META:
    -If not explicitly named, django will name the database tables "appname_modelname",
    for example "lettergame_alphabet". But in class META, the property 'db_table' allows
    for the naming of the table in the database. ** RECCOMENDED FOR EASE OF USE **
    -Managed: This property is a boolean. Essentially, default set to true. If set to False,
    migration will NOT add it to the database. The command 'inspectdb' returns it as False,
    since it already exists in the database.
    -See: https://docs.djangoproject.com/en/2.0/ref/models/options/

TROUBLESHOOTING:
-If you are having problems with migrations or models, try deleting the database and re-creating it.
 To do this, follow these steps:
    1. To collect the data currently in the database, use the following command

            python manage.py dumpdata > data.json

       This creates a json file in your current directory
    2. To drop and recreate the database, run the following:

            python manage.py dbshell
            drop database CreeTutordb;
            create database CreeTutordb;
            exit

    3. Next, migrate to recreate the models in models.py

            python manage.py migrate

    4. Then, using the data file we already created, repopulate the tables:

            python manage.py loaddata data.json

    Note: There will still be a json file with all of the data that was in the database that has
    all the data information from the database, which should be deleted.

'''

class Alphabet(models.Model):
    name = models.CharField(primary_key=True, max_length=2)
    vowel = models.TextField(blank=True, null=True)
    sound = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "alphabet"

class LettergameStats(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    chosen_answer = models.CharField(max_length=4, blank=True, null=True)
    correct_answer = models.CharField(max_length=4, blank=True, null=True)
    time_answered = models.DateTimeField(blank=True, null=True)



class LetterPairs(models.Model):
    name = models.CharField(primary_key=True, max_length=4)
    first_letter = models.CharField(max_length=2, blank=True, null=True)
    second_letter = models.CharField(max_length=2, blank=True, null=True)
    sound = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "letter_pairs"



class PairletterStats(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    chosen_answer = models.TextField(blank=True, null=True)
    correct_answer = models.TextField(blank=True, null=True)
    time_answered = models.DateTimeField(blank=True, null=True)


class SoundInSyl(models.Model):
    syl_id = models.IntegerField(blank=True, null=True)
    pair = models.CharField(max_length=8, blank=True, null=True)
    vowel = models.CharField(max_length=4, blank=True, null=True)


class WordSyllables(models.Model):
    word_id = models.IntegerField(blank=True, null=True)
    syllable_num = models.IntegerField(blank=True, null=True)
    syllable_name = models.TextField(blank=True, null=True)


class Word(models.Model):
    word = models.CharField(max_length=255)
    word_id = models.IntegerField(primary_key=True)
    num_syllables = models.IntegerField(blank=True, null=True)
    #lemma = models.ForeignKey
    #gram_code = models.ForeignKey
    #translation = models.CharField(max_length=40, null=True)



    class Meta:
        db_table = "words"

"""
class Lemma(models.Model):
    lemma = models.ForeignKey
    usable_gram_codes = models.manytomany(Gram_code())
    pos = models.CharField(max_length, null=True)
        #possible: V N IPC Pron Num
        #These are available in Linguistics/sorted_gram_codes.txt

    animate = models.CharField(max_length=25, null=True)
        #possible: AN IN null

    transitive = models.Charfield(max_length=25, null=True)
        #possible: II AI TI TA null

    translation = models.CharField(max_length=250, null=True)

class Gram_code(models.Model):
    gram_code = models.CharField(primary_key=True, max_length=100, unique=True)
"""
