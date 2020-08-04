from django.db import models

from lettergame.models import Lemma,Word,LemmaGame, recipe

class Affix(models.Model):
    '''
    Affix table contains the possible affixes that can be inflected on words. 
        - id            integer id
        - sro           affix written in standard roman orthography
        - syl           affix written in syllabics
        - translation   rough English translation of its meaning
    '''
    id = models.IntegerField(blank=False, null=False, primary_key=True)
    sro = models.CharField(max_length=255, blank=True, null=True)
    syl = models.CharField(max_length=255, blank=True, null=True)
    translation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'affix'

class Phrase(models.Model):
    '''
    Phrase table for a collection of grams that join together to make a phrase.
    A maximum of 5 grams can be included in one phrase. The columns are as follows
        - pid           integer id
        - gram_X        a word, FK to Word table
        - gram_X_prefix gram X's prefix, FK to Affix table
        - gram_X_suffix gram X's suffix, FK to Affix table
        - sound         sound file name related to the phrase
        - image         image file name related to the phrase
        - translation   translation, aka meaning of the phrase
    '''
    pid = models.IntegerField(blank=False, null=False, primary_key=True)

    gram_1 = models.ForeignKey(Word, models.DO_NOTHING, blank=True, null=True, related_name='gram_1')
    gram_1_prefix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_1_prefix')
    gram_1_suffix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_1_suffix')
    
    gram_2 = models.ForeignKey(Word, models.DO_NOTHING, blank=True, null=True, related_name='gram_2')
    gram_2_prefix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_2_prefix')
    gram_2_suffix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_2_suffix')
    
    gram_3 = models.ForeignKey(Word, models.DO_NOTHING, blank=True, null=True, related_name='gram_3')
    gram_3_prefix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_3_prefix')
    gram_3_suffix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_3_suffix')
    
    gram_4 = models.ForeignKey(Word, models.DO_NOTHING, blank=True, null=True, related_name='gram_4')
    gram_4_prefix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_4_prefix')
    gram_4_suffix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_4_suffix')
    
    gram_5 = models.ForeignKey(Word, models.DO_NOTHING, blank=True, null=True, related_name='gram_5')
    gram_5_prefix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_5_prefix')
    gram_5_suffix = models.ForeignKey(Affix, models.DO_NOTHING, blank=True, null=True, related_name='gram_5_suffix')

    sound = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    translation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'phrase'

class VocabLessons(models.Model):
    """
    Class contains Phrase information
    - "lesson_no" integer correlated to lesson number
    - "phrase" foreign key to Phrase table
    """
    lesson_no = models.IntegerField(blank=False, null=False)
    pid = models.ForeignKey(Phrase, models.DO_NOTHING, blank=False, null=True, related_name='phrase')
    
    class Meta:
        db_table = 'vocab_lessons'