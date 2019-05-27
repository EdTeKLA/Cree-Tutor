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
    characters_per_minute = models.FloatField(default=default_for_stats)
    number_of_words = models.IntegerField(default=default_for_stats)
    number_of_characters = models.IntegerField(default=default_for_stats)
    
    class Meta:
        db_table = "audio_and_subtitle_files_for_shadowing"
