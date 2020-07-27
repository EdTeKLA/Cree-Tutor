"""
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
-Creating a model(table) using mysql:
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
    for the re-naming of the table in the database. ** RECCOMENDED FOR EASE OF USE **
    -Managed: This property is a boolean. Essentially, default set to true. If set to False,
    migration will NOT add it to the database. The command 'inspectdb' returns it as False,
    since it already exists in the database.
    -See: https://docs.djangoproject.com/en/2.0/ref/models/options/

TROUBLESHOOTING:
-If you are having problems with migrations or models, try deleting the database and re-creating it.
 To do this, follow these steps:
    1. To collect the data currently in the database, navigate to `CreeTutor/CreeTutorBackEnd` run the following command:

            python manage.py dumpdata > data.json

       This creates a json file in your current directory

    2. To drop and recreate the database, run the following:

            python manage.py dbshell
            drop database CreeTutordb;
            create database CreeTutordb;
            exit

    3. Navigate to the director `CreeTutor/CreeTutorBackEnd/lettergame/migrations` and deleted
       everything EXCEPT the `__init__.py` file.

    4. From the directory `CreeTutor/CreeTutorBackEnd`, make all migrations for your
       models in models.py with the following command:

            python manage.py makemigrations

    5. Next, migrate with the following command:

            python manage.py migrate

    6. Then, using the data file we already created, repopulate the tables:

            python manage.py loaddata data.json

    Note: There will still be a json file with all of the data that was in the database that has
    all the data information from the database, which may be deleted.

"""

from django.db import models

from login.models import ModifiedUser


class GameLevels(models.Model):
    """
    Class describes what level the current games may operate at.
    - "level" is the level difficulty e.g. "easy", "medium", "hard"
    - "type" is the type of the level (e.g. "sro", "syllabic)
    - "description" describes what makes it that level (e.g. "contains __ number of distractors of type __")
    """

    level = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'game_levels'


class LetterGameOrPairGameSession(models.Model):
    """
    Start and end of a session is logged here with the level at which the session was done at.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(ModifiedUser, on_delete=models.CASCADE)
    session_begin = models.DateTimeField(blank=True, null=True)
    session_end = models.DateTimeField(blank=True, null=True)
    level = models.ForeignKey(GameLevels, on_delete=models.CASCADE)

    class Meta:
        db_table = 'letter_game_or_pair_game_session'

class Alphabet(models.Model):
    """
    Class contains the Standard Roman Orthography for Plains Cree.
    - "letter" is self explanitory and is primary key (e.g. "a")
    - "vowel" is class of speech sound (i.e. "vowel", "semi-vowel", "consonant")
    - "sound" contains the path to the recording of the letter
    """

    letter = models.CharField(primary_key=True, max_length=2)
    vowel = models.TextField(blank=True, null=True)
    sound = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "alphabet"

class LetterUserSeen(models.Model):
    """
    Class contains letters that a user has seen at least once.
    - "user_id" identifies user
    - "letter" identifies which letter user has seen
    - "amount_seen" counts the amount of times this has been seen
    Other information can be found in the stats models of single letter games.
    """

    user_id = models.IntegerField(blank=True, null=True)
    letter = models.ForeignKey(Alphabet, models.DO_NOTHING, db_column='letter')
    amount_seen = models.IntegerField(default = 0, blank=True, null=True)

    # def initalize(self):
    #     all_letters = Alphabet.object.all()
    #     for i in all_letters

    class Meta:
        db_table = "letter_user_seen"
        unique_together = (('user_id', 'letter'),)


class LetterPair(models.Model):
    """
    Class contains pairs of letters from Standard Roman Orthography for Plains Cree.
    - "pair" is the pair of letters and is primary key (e.g. "aw")
    - "first_letter"/"second_letter" contain the first and second letters, respectively, of the letter pair.
    - "sound" contains the path to the recording of the pair
    """

    pair = models.CharField(primary_key=True, max_length=4)
    first_letter = models.ForeignKey(Alphabet, models.DO_NOTHING, db_column='first_letter', blank=True, null=True)
    second_letter = models.ForeignKey(Alphabet, models.DO_NOTHING, db_column='second_letter', blank=True, null=True, related_name = '+')
    sound = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'letter_pair'


class PairUserSeen(models.Model):
    """
    Class contains letter pairs that a user has seen at least once.
    - "user_id" identifies user
    - "pair" identifies which pair user has seen
    """

    user_id = models.IntegerField(blank=True, null=True)
    pair = models.ForeignKey(LetterPair, models.DO_NOTHING, db_column='pair')

    class Meta:
        db_table = "pair_user_seen"
        unique_together = (('user_id', 'pair'),)


class DistractorType(models.Model):
    """
    Class describes in what way an object might be distracting.
    - "type" is the integer id and primary key (e.g. 1)
    - "distraction" describes how it is distracting (e.g. "audiovisual", "dissimilar")
    - "insro" dictates whether the distraction is in Cree SRO (i.e. "yes", "no")
    """

    type = models.IntegerField(primary_key=True)
    distraction = models.TextField(blank=True, null=True)
    insro = models.CharField(db_column='insro', max_length=8, blank=True, null=True)

    class Meta:
        db_table = 'distractor_type'


class PairDistractor(models.Model):
    """
    Class contains pairs from the class "LetterPair" and conrresponding distractor pairs.
    - "pair" is simply an SRO pair from class "LetterPair" (e.g. "ka")
    - "distractor" is a pair of letters which may or may not be in SRO (e.g. "ga")
    - "type" refers to the types of distractors described in class DistractorType
    """

    pair = models.ForeignKey(LetterPair, models.DO_NOTHING, db_column='pair')
    distractor = models.CharField(max_length=16)
    type = models.ForeignKey(DistractorType, models.DO_NOTHING, db_column='type', blank=True, null=True)

    class Meta:
        db_table = 'pair_distractor'
        unique_together = (('pair', 'distractor'),)


class PartOfSpeech(models.Model):
    """
    Class defines possible options for describing "part of speech"
    Possibilities are restricted to:
            V N IPC Pron Num
    """

    pos = models.CharField(primary_key=True, max_length=10)

    class Meta:
        db_table = "part_of_speech"

class Transitive(models.Model):
    """
    Class defines possible options for describing transitivity of verbs
    Possibilities are restricted to:
            II AI TI TA NULL
            TODO: Spell out what each option is
    """

    transitive = models.CharField(primary_key=True, max_length=8)

    class Meta:
        db_table = "transitive"


class Animate(models.Model):
    """
    Class defines possible options for describing animacy of nouns
    Possibilities are restricted to:
            AN IN NULL
    """

    animate = models.CharField(primary_key=True, max_length=25)

    class Meta:
        db_table = "animate"

class GramCode(models.Model):
    """
    Class defines possible options for grammar codes.
    Possibilities are defined and are available in Linguistics/sorted_gram_codes.txt
    """

    gram_code = models.CharField(primary_key=True, max_length=100, unique=True)

    class Meta:
        db_table = "gram_code"


class SingleLetterStats(models.Model):
    """
    Class contains related information logged when users play the "Single Letter Game".
    - "answer_id" is the integer ID and primary key. Is automatically incremented.
    - "user_id" identifies user.
    - "level" identifies which level the user is playing the game at, levels are defined in class GameLevels
    - "chosen_answer" is the answer the user chose
    - "correct_answer" is the correct answer
    - "time_started" is the time, in ISO format, that the user started the specific question
    - "time_ended" is the time, in ISO format, that the user ended the specific question
    """

    answer_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    level = models.ForeignKey(GameLevels, models.CASCADE, null=True, db_column='level')
    chosen_answer = models.CharField(max_length=4, blank=True, null=True)
    correct_answer = models.CharField(max_length=4, blank=True, null=True)
    time_started = models.DateTimeField(blank=True, null=True)
    time_ended = models.DateTimeField(blank=True, null=True)
    session = models.ForeignKey(LetterGameOrPairGameSession, on_delete=models.CASCADE)

    class Meta:
        db_table = "single_letter_stats"


class SLSDistractedBy(models.Model):
    """
    Class contains logged interactions of user hovering over potential answers when playing the "Single Letter Game".
    - "answer_id" refers to the primary key of the class SingleLetterStats
    - "distracted_by" is the potential answer the user hovered over
    - "time_hover_start" is the time, in ISO format, that the user started hovering over potential answer
    - "time_hover_end" is the time, in ISO format, that the user ended hovering over potential answer
    """

    answer_id = models.ForeignKey(SingleLetterStats, models.DO_NOTHING, null=True, db_column='answer_id')
    distracted_by = models.ForeignKey(Alphabet, models.DO_NOTHING, db_column='letter')
    time_hover_start = models.DateTimeField(blank=True, null=True)
    time_hover_end = models.DateTimeField(blank=True, null=True)
    session = models.ForeignKey(LetterGameOrPairGameSession, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "sls_distractedby"
        unique_together = (('answer_id', 'distracted_by', 'time_hover_start'),)


class SLSDistractors(models.Model):
    """
    Class contains the incorrect options given to user as distractors when playing "Single Letter Game".
    - "answer_id" refers to the primary key of the class SingleLetterStats
    - "distractor" refers to the incorrect option given
    """

    answer_id = models.ForeignKey(SingleLetterStats, models.DO_NOTHING, null=True, db_column='answer_id')
    distractor = models.ForeignKey(Alphabet, models.DO_NOTHING, db_column='letter')
    session = models.ForeignKey(LetterGameOrPairGameSession, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'sls_distractors'
        unique_together = (('answer_id', 'distractor'))


class LetterDistractor(models.Model):
    """
    Class contains pairs from the class "LetterPair" and conrresponding distractor pairs.
    - "pair" is simply an SRO letter from class "Alphabet" (e.g. "t")
    - "distractor" is a letter which may or may not be in SRO (e.g. "d")
    - "type" refers to the types of distractors described in class DistractorType
    """

    letter = models.ForeignKey(Alphabet, models.DO_NOTHING, db_column='letter')
    distractor = models.CharField(max_length=4)
    type = models.ForeignKey(DistractorType, models.DO_NOTHING, db_column='type', blank=True, null=True)

    class Meta:
        db_table = 'letter_distractor'
        unique_together = (('letter', 'distractor'),)


class DoubleLetterStats(models.Model):
    """
    Class contains related information logged when users play the "Double Letter Game".
    - "answer_id" is the integer ID and primary key. Is automatically incremented.
    - "user_id" identifies user.
    - "level" identifies which level the user is playing the game at, levels are defined in class GameLevels
    - "chosen_answer" is the answer the user chose
    - "correct_answer" is the correct answer
    - "time_started" is the time, in ISO format, that the user started the specific question
    - "time_ended" is the time, in ISO format, that the user ended the specific question
    """

    answer_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    level = models.ForeignKey(GameLevels, models.CASCADE, null=True, db_column='level')
    chosen_answer = models.TextField(blank=True, null=True)
    correct_answer = models.TextField(blank=True, null=True)
    time_started = models.DateTimeField(blank=True, null=True)
    time_ended = models.DateTimeField(blank=True, null=True)
    session = models.ForeignKey(LetterGameOrPairGameSession, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "double_letter_stats"


class DLSDistractedBy(models.Model):
    """
    Class contains logged interactions of user hovering over potential answers when playing the "Double Letter Game".
    - "answer_id" refers to the primary key of the class DoubleLetterStats
    - "distracted_by" is the potential answer the user hovered over
    - "time_hover_start" is the time, in ISO format, that the user started hovering over potential answer
    - "time_hover_end" is the time, in ISO format, that the user ended hovering over potential answer
    """

    answer_id = models.ForeignKey(DoubleLetterStats, models.DO_NOTHING, null=True, db_column='answer_id')
    distracted_by = models.ForeignKey(LetterPair, models.DO_NOTHING, db_column='pair')
    time_hover_start = models.DateTimeField(blank=True, null=True)
    time_hover_end = models.DateTimeField(blank=True, null=True)
    session = models.ForeignKey(LetterGameOrPairGameSession, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "dls_distractedby"
        unique_together = (('answer_id', 'distracted_by', 'time_hover_start'),)


class DLSDistractors(models.Model):
    """
    Class contains the incorrect options given to user as distractors when playing "Double Letter Game".
    - "answer_id" refers to the primary key of the class DoubleLetterStats
    - "distractor" refers to the incorrect option given
    """

    answer_id = models.ForeignKey(DoubleLetterStats, models.DO_NOTHING, null=True, db_column='answer_id')
    distractor = models.ForeignKey(LetterPair, models.DO_NOTHING, db_column='pair')
    session = models.ForeignKey(LetterGameOrPairGameSession, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'dls_distractors'
        unique_together = (('answer_id', 'distractor'))


class Lemma(models.Model):
    """
    Class contains necessary properties to describe a lemma.
    - "id" contains integer ID and primary key.
    - "lemma" is the SRO spelling of lemma.
    - "useable_gram_codes" is the applicable grammar codes as described in class GramCode
    - "pos" is the appropriate part of speech, as described in class PartOfSpeech
    - "animate" describes the animacy of lemma, as described in class Animate
    - "transitive" describes the transitivity of lemma, as described in class Transitive
    - "translation" contains the english translation
    - "image" contains the path to a related descriptive image
    """

    id = models.IntegerField(primary_key=True)
    lemma = models.CharField(max_length=255, blank=True, null=True)
    useable_gram_codes = models.ForeignKey(GramCode, models.DO_NOTHING, blank=True, null=True)
    pos = models.ForeignKey(PartOfSpeech, models.DO_NOTHING, blank=True, null=True)
    animate = models.ForeignKey(Animate, models.DO_NOTHING, blank=True, null=True)
    transitive = models.ForeignKey(Transitive, models.DO_NOTHING, blank=True, null=True)
    translation = models.CharField(max_length=250, blank=True, null=True)
    image = models.CharField(max_length=250, blank=True, null=True)


    def __str__(self):
        return self.lemma + " " + str(self.id)

    class Meta:
        db_table = 'lemma'


class Word(models.Model):
    """
    Class contains necessary properties to describe a word form.
    - "word_id" contains integer ID and primary key.
    - "word" is the SRO spelling of word form.
    - "gram_code" is the applicable grammar codes as described in class GramCode
    - "translation" contains the english translation
    - "num_syllables" is, loosely, the number of syllables in the word
    - "lemmaID" is the integer id referring to the relevant lemma descibed in the class Lemma
    - "sound" contains the path to the recording of the word
    """

    word_id = models.IntegerField(primary_key=True, default=0)
    word = models.CharField(max_length=255, blank=True, null=True)
    gram_code = models.ForeignKey(GramCode, models.DO_NOTHING, blank=True, null=True)
    translation = models.TextField(blank=True, null=True)
    num_syllables = models.IntegerField(blank=True, null=True)
    lemmaid = models.ForeignKey(Lemma, models.DO_NOTHING, blank=True, null=True)
    sound = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.word + " " + str(self.word_id)

    class Meta:
        db_table = 'word'


class LemmaGame(models.Model):
    """
    Class contains three foriegn keys that are used in the lemmagame views
    "wordform" links to a word object, which specifies which wordform will appear
    "lemma" links to a lemma objects, which specifies almost everything else
    "distractors" is a number of word objects to use as distractors
    """
    #For Nouns, this should default to the non-affixed noun, e.i. atim+N+AN+Sg -> atim
    wordform = models.ForeignKey(Word, models.DO_NOTHING,blank=True, null=True)
    lemma = models.ForeignKey(Lemma, models.DO_NOTHING, blank=False, null=True)
    distractors = models.ManyToManyField(Word, related_name="+")


    def __str__(self):
        return self.wordform.word

    class Meta:
        db_table = 'lemma_game'


class Creedictionarydotcom(models.Model):
    """
    Temporary class used for manupulating words scraped from creedictionary.com
    Scraped data NOT to be pushed to github
    """

    word = models.CharField(primary_key=True, max_length=250)
    plural = models.CharField(max_length=250, blank=True, null=True)
    syllabics = models.TextField(blank=True, null=True)
    pos = models.CharField(max_length=50)
    translation = models.CharField(max_length=250)
    dictionary = models.CharField(max_length=8)

    class Meta:
        db_table = 'creedictionarydotcom'
        unique_together = (('word', 'pos', 'translation', 'dictionary'),)

class invadersSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(ModifiedUser, on_delete=models.CASCADE)
    sessionBegin = models.DateTimeField(blank=True, null=True)
    level = models.CharField(max_length=8, blank=True)

    class Meta:
        db_table = "invaders_session"
        unique_together = (("sessionBegin", "user"),)

class invadersStats(models.Model):
    sesh_id = models.ForeignKey(invadersSession, on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(blank=True, null=True)
    letter = models.CharField(max_length=8)
    correct = models.CharField(max_length=8)
    screen_position = models.CharField(max_length=20)
    hit_or_left = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'invaders_stats'

class invadersUserCorrect(models.Model):
    sesh_id = models.ForeignKey(invadersSession, on_delete=models.CASCADE)
    letter = models.CharField(max_length=8)

    class Meta:
        db_table = "invaders_user_correct"



#________ The following classes are being set up to create games for listening to specific sounds within words ________#

# class SoundInSyllable(models.Model):
#     syl_id = models.IntegerField(blank=True, null=True)
#     pair = models.CharField(max_length=8, blank=True, null=True)
#     vowel = models.CharField(max_length=4, blank=True, null=True)
#
#     class Meta:
#         db_table = "sound_in_syllable"
#
#
# class WordSyllable(models.Model):
#     word_id = models.IntegerField(blank=True, null=True)
#     syllable_num = models.IntegerField(blank=True, null=True)
#     syllable_name = models.TextField(blank=True, null=True)
#
#     class Meta:
#         db_table = "word_syllable"

class recipe(models.Model):
    prefix = models.CharField(max_length=3, blank=True)
    suffix = models.CharField(max_length=15)
    independent_or_conjunct = models.CharField(max_length=200)
    special_rule = models.CharField(max_length=200, blank=True)
    joiner = models.CharField(max_length=20, blank=True)
    pronoun = models.CharField(max_length=3)
    paradigm = models.CharField(max_length=25)
    translation = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "burger_game_phrases"

class burgerSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(ModifiedUser, on_delete=models.CASCADE)
    sessionBegin = models.DateTimeField(blank=True, null=True)
    session_difficulty = models.CharField(blank=True,default="easy", max_length=30)
    session_time_limit = models.IntegerField(default="300000")


class burgerStats(models.Model):
    sesh_id = models.ForeignKey(burgerSession, on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(blank=True, null=True)
    prefixes = models.CharField(max_length=100)
    suffixes = models.CharField(max_length=100)
    verbs = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'burger_stats'


class conjugationBurgerStats(models.Model):
    sesh_id = models.ForeignKey(burgerSession, on_delete=models.CASCADE, null=True)
    conjugation = models.CharField(max_length=200)

class verbBurgerStats(models.Model):
    sesh_id = models.ForeignKey(burgerSession, on_delete=models.CASCADE, null=True)
    right_verb = models.CharField(max_length=200)

class playerChoseBurgerStats(models.Model):
    sesh_id = models.ForeignKey(burgerSession, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=1000, null=True)


