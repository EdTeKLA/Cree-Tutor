from datetime import datetime
from django.db import models

from common_to_apps.models import GeneralConfig, MediaAndSubtitleFiles, \
    UserStatsForCharacterPerMinute, LogActionsInActivityWhereMarkingIsOnSlidingScale, FeedbackQuestions, \
    LogFeedBackAnswers


class ShadowingConfig(GeneralConfig):
    """
    Model was created to store the config for the shadowing app.
    """
    class Meta:
        db_table = "shadowing_config"


class AudioAndSubtitleFilesForShadowing(MediaAndSubtitleFiles):
    """
    Model is created to store all the files we could use for Shadowing and the level
    """
    class Meta:
        db_table = "shadowing_audio_and_subtitle_files"


class ShadowingUserStats(UserStatsForCharacterPerMinute):
    """
    Class was created to store user stats, depends on how they did in the past.
    """
    class Meta:
        db_table = "shadowing_user_stats"


class ShadowingLogActions(LogActionsInActivityWhereMarkingIsOnSlidingScale):
    """
    Model was created to log a user's interactions with a story. Can include
        - Play
        - Pause
        - Selection
        - Finished

    The logging happens when a user click on the title of a story on at /shadowing/
    """
    # Name of the story, the story to which this action is attached to
    story = models.ForeignKey(
        AudioAndSubtitleFilesForShadowing, on_delete=models.CASCADE)
    # The time at which the action took place during the recording, in milliseconds
    story_time = models.FloatField()

    class Meta:
        db_table = "shadowing_log_actions"


class ShadowingFeedbackQuestions(FeedbackQuestions):
    """
    Model was created to store question that we will ask the user after a reading is finished.
    """
    class Meta:
        db_table = "shadowing_feedback_questions"


class ShadowingLogFeedbackAnswers(LogFeedBackAnswers):
    """
    Models was created to log the responses of the user to feedback questions.
    """
    # Which story this feed back is connected to
    story = models.ForeignKey(
        AudioAndSubtitleFilesForShadowing, on_delete=models.DO_NOTHING)
    # The question that was answered
    question = models.ForeignKey(
        ShadowingFeedbackQuestions, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "shadowing_log_feedback_answers"
