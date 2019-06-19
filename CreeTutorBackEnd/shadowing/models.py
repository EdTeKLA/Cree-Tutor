from datetime import datetime
from django.contrib.auth.models import User

from django.db import models


class ShadowingConfig(models.Model):
    """
    Model was created to store the config for the shadowing app.
    """
    # The name of the configuration
    name = models.TextField(null=False, blank=False, unique=True)
    # The configuration settings, is a text field, but will store numbers as well
    config = models.TextField(null=False, blank=False)

    class Meta:
        db_table = "shadowing_config"

class AudioAndSubtitleFilesForShadowing(models.Model):
    """
    Model is created to store all the files we could use for Shadowing and the level
    """
    # The id/primary key
    id = models.BigAutoField(primary_key=True)
    # Name of the story
    name = models.TextField(unique=True)
    # The location of the subtitles
    sub_location = models.TextField(unique=True)
    # The location of the sound file
    sound_location = models.TextField(unique=True)

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
        db_table = "audio_and_subtitle_files_for_shadowing"


class ShadowingFeedbackQuestions(models.Model):
    """
    Model was created to store question that we will ask the user after a reading is finished.
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
        db_table = "shadowing_feedback_questions"


class ShadowingUserStats(models.Model):
    """
    Class was created to store user stats, depends on how they did in the past.
    """
    # The id/primary key
    id = models.BigAutoField(primary_key=True)
    # The user for which the stats exist
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The stats
    default_for_stats = 0
    chars_per_minute = models.FloatField(default=default_for_stats)

    class Meta:
        db_table = "shadowing_user_stats"


class ShadowingLogActions(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Name of the story
    story = models.ForeignKey(AudioAndSubtitleFilesForShadowing, on_delete=models.CASCADE)
    # The time at which the action took place during the recording, in milliseconds
    story_time = models.FloatField()
    # What the person did
    action = models.TextField()
    # When the person clicked the button
    time = models.DateTimeField(default=datetime.now)
    # Session id will be a guid
    session_id = models.TextField()

    class Meta:
        db_table = "shadowing_log_actions"


class ShadowingLogFeedbackAnswers(models.Model):
    """
    Models was created to log the responses of the user to feedback questions.
    """
    # The user that answered the question
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Which story this feed back is connected to
    story = models.ForeignKey(AudioAndSubtitleFilesForShadowing, on_delete=models.DO_NOTHING)
    # The question that was answered
    question = models.ForeignKey(ShadowingFeedbackQuestions, on_delete=models.DO_NOTHING)
    # The answers, whether it was yes/no or could/could not, etc
    answer = models.BooleanField()
    # The time at which the the feedback was given
    time = models.DateTimeField(default=datetime.now)
    # Session id will be a guid
    session_id = models.TextField()

    class Meta:
        db_table = "shadowing_log_feedback_answers"