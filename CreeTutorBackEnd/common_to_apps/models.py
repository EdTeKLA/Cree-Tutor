from datetime import datetime

from django.db import models
from CreeTutorBackEnd.settings import AUTH_USER_MODEL


class GeneralConfig(models.Model):
    """
    Model was created to store the config for apps. This is as general as possible, that is what both name and config
    are text fields.
    """
    # The name of the configuration
    name = models.TextField(null=False, blank=False, unique=True)
    # The configuration settings, is a text field, but will store numbers as well
    config = models.TextField(null=False, blank=False)

    class Meta:
        abstract = True


class UserStatsForCharacterPerMinute(models.Model):
    """
    Class was created to store user stats, depends on how they did in the past.
    """
    # The id/primary key
    id = models.BigAutoField(primary_key=True)
    # The user for which the stats exist
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    # The stats
    default_for_stats = 0
    # Stores how well the user is doing, which character rate should be used as the center point of the next bracket
    chars_per_minute = models.FloatField(default=default_for_stats)

    class Meta:
        abstract = True


class MediaAndSubtitleFiles(models.Model):
    """
    Model is created to store all the media files, their srt files and stats related to these files for
    transcription and shadowing.
    """
    # The id/primary key
    id = models.BigAutoField(primary_key=True)
    # Name of the story
    name = models.TextField(unique=True)
    # The location of the subtitles
    sub_location = models.TextField(unique=True)
    # The location of the sound file
    media_location = models.TextField(unique=True)

    # File stats
    default_for_stats = 0
    mean = models.FloatField(default=default_for_stats)
    median = models.FloatField(default=default_for_stats)
    min = models.FloatField(default=default_for_stats)
    max = models.FloatField(default=default_for_stats)
    words_per_minute = models.FloatField(default=default_for_stats)
    chars_per_minute = models.FloatField(default=default_for_stats)
    number_of_words = models.IntegerField(default=default_for_stats)
    number_of_chars = models.IntegerField(default=default_for_stats)

    class Meta:
        abstract = True


class LogActionsInActivityWhereMarkingIsOnSlidingScale(models.Model):
    """
    Model was created to log a user's interactions with a story. Can include
        - Play
        - Pause
        - Selection
        - Finished

    The logging happens when a user click on the title of a story on at /shadowing/
    """
    # The id/primary key
    id = models.BigAutoField(primary_key=True)
    # The user this is connected to
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # What the person did
    action = models.TextField()
    # When the person clicked the button
    time = models.DateTimeField(default=datetime.now)
    # Session id will be a guid
    session_id = models.TextField()

    class Meta:
        abstract = True


class FeedbackQuestions(models.Model):
    """
    Model was created to store question that the user will be asked when self assessment for an activity is required.
    """
    # The id/primary key
    id = models.BigAutoField(primary_key=True)
    # Name of the story
    question = models.TextField(unique=True)
    # The location of the subtitles
    yes_answer = models.TextField()
    # The location of the sound file
    no_answer = models.TextField()

    class Meta:
        abstract = True


class LogFeedBackAnswers(models.Model):
    """
    Models was created to log the responses of the user to feedback questions.
    Two fields needs to defined after this, they are named:
        - story(subclass of MediaAndSubtitleFiles)
        - question(subclass of FeedbackQuestions)
    """
    # The user that answered the question
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # The answers, whether it was yes/no or could/could not, etc
    answer = models.BooleanField()
    # The time at which the the feedback was given
    time = models.DateTimeField(default=datetime.now)
    # Session id will be a guid
    session_id = models.TextField()

    class Meta:
        abstract = True
