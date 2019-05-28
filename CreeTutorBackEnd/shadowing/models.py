from django.db import models


# Create your models here.
class AudioAndSubtitleFilesForShadowing(models.Model):
    """
    Model is created to store all the files we could use for Shadowing and the level
    """
    # The id/primary key
    id = models.BigAutoField(primary_key=True)
    # Name of the story
    name = models.TextField()
    # The location of the subtitles
    sub_location = models.TextField()
    # The location of the sound file
    sound_location = models.TextField()
    class Meta:
        db_table = "audio_and_subtitle_files_for_shadowing"
