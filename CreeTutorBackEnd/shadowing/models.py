from datetime import datetime

from django.db import models


# Create your models here.
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

class ShadowingUserStats:
    pass

class ShadowingLogStorySelection(models.Model):
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
    # Name of the story
    story_id = models.ForeignKey(AudioAndSubtitleFilesForShadowing, on_delete=models.CASCADE)
    # When the person clicked the button
    time = models.DateTimeField(default=datetime.now)
    # The time at which the action took place during the recording
    story_time = models.DateTimeField

    class Meta:
        db_table = "shadowing_log_story_selection"
