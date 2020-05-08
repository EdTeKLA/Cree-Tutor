from django.db import models
from login.models import ModifiedUser
from datetime import datetime


from common_to_apps.models import GeneralConfig, UserStatsForCharacterPerMinute, MediaAndSubtitleFiles, \
    LogActionsInActivityWhereMarkingIsOnSlidingScale, LogFeedBackAnswers, FeedbackQuestions


class TranscriptionConfig(GeneralConfig):
    """
    Model was created to store the config for the transcription app.
    """
    class Meta:
        db_table = "transcription_config"


class TranscriptionUserStats(UserStatsForCharacterPerMinute):
    """
    Class was created to store user stats, depends on how they did in the past.
    """
    default_for_stats = 0
    # Stores how accurate the user has been so far in the transcription activity
    accuracy = models.FloatField(default=default_for_stats)
    # Final transcription, set to true if this was saved at the end, otherwise set to false
    final = models.BooleanField(null=False, blank=False, default=False)
    class Meta:
        db_table = "transcription_user_stats"


class VideoAndSubtitleFilesForTranscription(MediaAndSubtitleFiles):
    """
    Model is created to store all the files we could use for Transcription
    """
    class Meta:
        db_table = "transcription_video_and_subtitle_files"


class TranscriptionLogActions(LogActionsInActivityWhereMarkingIsOnSlidingScale):
    """
    Model was created to log a user's interactions with a story. Can include
        - Play
        - Pause
        - Selection
        - Finished
    The logging happens when a user click on the title of a story on at /shadowing/
    """
    # Name of the story
    story = models.ForeignKey(
        VideoAndSubtitleFilesForTranscription, on_delete=models.CASCADE)
    # The time at which the action took place during the recording, in milliseconds
    story_time = models.FloatField()
    # Stores what the transcription at the time looked like
    transcription = models.TextField()

    class Meta:
        db_table = "transcription_log_actions"


class TranscriptionFeedbackQuestions(FeedbackQuestions):
    """
    Model was created to store question that we will ask the user after a reading is finished.
    """
    class Meta:
        db_table = "transcription_feedback_questions"


class TranscriptionLogFeedbackAnswers(LogFeedBackAnswers):
    """
    Models was created to log the responses of the user to feedback questions.
    """
    # Which story this feed back is connected to
    story = models.ForeignKey(
        VideoAndSubtitleFilesForTranscription, on_delete=models.DO_NOTHING)
    # The question that was answered
    question = models.ForeignKey(
        TranscriptionFeedbackQuestions, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "transcription_log_feedback_answers"
