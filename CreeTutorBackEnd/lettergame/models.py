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
class PartOfSpeech(models.Model):
    #possible: V N IPC Pron Num
    pos = models.CharField(primary_key=True, max_length=10)

    class Meta:
        db_table = "part_of_speech"

class Transitive(models.Model):
    #possible: II AI TI TA null
    transitive = models.CharField(primary_key=True, max_length=8)

    class Meta:
        db_table = "transitive"

class Animate(models.Model):
    #possible: AN IN null
    animate = models.CharField(primary_key=True, max_length=25)

    class Meta:
        db_table = "animate"

class GramCode(models.Model):
    #These are available in Linguistics/sorted_gram_codes.txt
    gram_code = models.CharField(primary_key=True, max_length=100, unique=True)

    class Meta:
        db_table = "gram_code"

class Alphabet(models.Model):
    letter = models.CharField(primary_key=True, max_length=2)
    vowel = models.TextField(blank=True, null=True)
    sound = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "alphabet"

class SingleLetterStats(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    chosen_answer = models.CharField(max_length=4, blank=True, null=True)
    correct_answer = models.CharField(max_length=4, blank=True, null=True)
    time_answered = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "single_letter_stats"


class LetterPair(models.Model):
    pair = models.CharField(primary_key=True, max_length=4)
    first_letter = models.ForeignKey(Alphabet, models.DO_NOTHING, db_column='first_letter', blank=True, null=True)
    second_letter = models.ForeignKey(Alphabet, models.DO_NOTHING, db_column='second_letter', blank=True, null=True, related_name = '+')
    sound = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'letter_pair'


class DoubleLetterStats(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    chosen_answer = models.TextField(blank=True, null=True)
    correct_answer = models.TextField(blank=True, null=True)
    time_answered = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "double_letter_stats"


class SoundInSyllable(models.Model):
    syl_id = models.IntegerField(blank=True, null=True)
    pair = models.CharField(max_length=8, blank=True, null=True)
    vowel = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        db_table = "sound_in_syllable"


class WordSyllable(models.Model):
    word_id = models.IntegerField(blank=True, null=True)
    syllable_num = models.IntegerField(blank=True, null=True)
    syllable_name = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "word_syllable"


class Lemma(models.Model):
    id = models.IntegerField(primary_key=True)
    lemma = models.CharField(max_length=255, blank=True, null=True)
    useable_gram_codes = models.ForeignKey(GramCode, models.DO_NOTHING, blank=True, null=True)
    pos = models.ForeignKey(PartOfSpeech, models.DO_NOTHING, blank=True, null=True)
    animate = models.ForeignKey(Animate, models.DO_NOTHING, blank=True, null=True)
    transitive = models.ForeignKey(Transitive, models.DO_NOTHING, blank=True, null=True)
    translation = models.CharField(max_length=250, blank=True, null=True)
    image = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'lemma'

class Word(models.Model):
    word_id = models.IntegerField(primary_key=True, default=0)
    word = models.CharField(max_length=255, blank=True, null=True)

    gram_code = models.ForeignKey(GramCode, models.DO_NOTHING, blank=True, null=True)
    translation = models.TextField(blank=True, null=True)
    num_syllables = models.IntegerField(blank=True, null=True)
    lemmaID = models.ForeignKey(Lemma, models.DO_NOTHING, blank=True, null=True)
    sound = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'word'


class LemmaGame(models.Model):
    #For Nouns, this should default to the non-affixed noun, e.i. atim+N+AN+Sg -> atim
    wordform = models.ForeignKey(Word, models.DO_NOTHING,blank=True, null=True)

    lemma = models.ForeignKey(Lemma, models.DO_NOTHING, blank=False, null=True)

    distractors = models.ManyToManyField(Word, related_name="+")


    class Meta:
        db_table = 'lemma_game'
