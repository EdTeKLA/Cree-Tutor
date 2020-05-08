import os
import uuid
from time import strftime, gmtime
import json
import math

from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View

from common_to_apps.view_specialized_for_character_per_minute_activities import \
    IndexForListOfChoicesInWindowForUserStatsForCharacterPerMinuteOrSubclasses
from common_to_apps.subtitle_readers import SubtitleReader

from transcription.models import TranscriptionConfig, TranscriptionUserStats, VideoAndSubtitleFilesForTranscription,\
    TranscriptionFeedbackQuestions, TranscriptionLogFeedbackAnswers
from django.db.models import Min, F, Max

# Transcription:
# Log revisions
# Log back spaces
# Auto pauses
# Auto plays
# Word per word stats
# ????? Break the sentences up into words, add to db and use to store stats

# Send audio back to server, see the best size for how big the chunks should be so that the user does not click away in the end if too long
from transcription.models import TranscriptionLogActions


class Index(IndexForListOfChoicesInWindowForUserStatsForCharacterPerMinuteOrSubclasses):
    """
    Renders and shows the list of stories in the db.
    """
    config_class = TranscriptionConfig
    user_stats_class = TranscriptionUserStats
    media_table_to_filter_from = VideoAndSubtitleFilesForTranscription
    template_to_render = 'transcription/index.html'
    size_of_window_config = 'SLIDING_WINDOW_SIZE_FOR_FETCH'
    min_number_of_choices_config = 'MIN_NUMBER_OF_CHOICES'


class Transcription(View):
    """

    """

    def get(self, request, story_index):
        """
        Gets the requested story, processes the text and renders the story tempalte
        :param request:
        :param story_index:
        :return:
        """
        try:
            story_info = VideoAndSubtitleFilesForTranscription.objects.get(id=story_index)

            module_dir = os.path.dirname(__file__)  # get current directory
            file_path = os.path.join(module_dir, story_info.sub_location)
            transcript = SubtitleReader.read_file(file_path, sentences=True)

            # Break transcription into sentences and letters
            sentences_and_letters = []
            for i in range(0, len(transcript)):
                letters = []
                for j in range(0, len(transcript[i][3])):
                    letters.append([i, j, transcript[i][3][j]])

                sentences_and_letters.append([i, letters])
            print(sentences_and_letters)
            context = {"video_file_loc": story_info.media_location,
                       "video_transcript_list": transcript,
                       "split_sentences": sentences_and_letters,
                       "story_id": story_index,
                       "session_id": uuid.uuid4()}
            return render(request, 'transcription/story.html', context)
        except VideoAndSubtitleFilesForTranscription.DoesNotExist:
            return HttpResponseNotFound("Page Not Found")


class TranscriptionLogging(View):
    """
    Only takes post request. Logs the information for the shadowing questions.
    """
    def post(self, request, story_id, action, time, session_id, transcription):
        """
        Logs the information for shadowing. This includes the information in ShadowingLogStorySelection model.
        :param request:
        :param story_id:
        :param action:
        :param time:
        :return:
        """
        # Keep in mind, if any letter in transcription == þ, that letter actually equals ', ", ’, “, ”, ‘
        # Bug in browsers keeps from getting letter as one of those.
        # If ~ is transcription, then it is empty
        if transcription == "~":
            transcription = ""

        # Attempts to log the action and returns the status
        try:
            log = TranscriptionLogActions(
                user=request.user,
                story_id=story_id,
                action=action,
                story_time=time,
                time=strftime('%Y-%m-%d %H:%M:%S.%s%z', gmtime()),
                session_id=session_id,
                transcription=transcription
            )

            log.save()
            return JsonResponse({"status": "success"})
        except:
            return JsonResponse({"status": "error"})


class ShadowingFeedBack(View):
    """
    Renders the answers.

    Saves the logs for how the person answered and updates the values of what where they score is.
    """
    def get(self, request, story_id, session_id):
        """
        Gets all the questions from the database for shadowing questions and puts it into a context to show the user.
        :param request:
        :param story_id:
        :return:
        """
        questions = TranscriptionFeedbackQuestions.objects.all()

        # Create the context and render
        context = { "story_id": story_id, "questions": questions, "session_id":session_id }
        return render(request, 'transcription/feedback.html', context)

    def post(self, request, story_id, session_id):
        """
        Logs all the answers to the question of the person and updates the stats of the user depending on their
        feedback.
        :param request:
        :param story_id:
        :return:
        """
        # The amount the score will be changed by at the start
        # This number will be decayed over time, using alpha
        change_score_by_constant = float(TranscriptionConfig.objects.get(name='CHANGE_SCORE_BY').config)
        # Variables hold the number of question that will change the person's score up or down
        yes_ratio_for_increase = float(TranscriptionConfig.objects.get(name='TRANSCRIPTION_RATE_TO_INCREASE_SCORE')
                                       .config)
        no_ratio_for_decrease = float(TranscriptionConfig.objects.get(name='TRANSCRIPTION_RATE_TO_DECREASE_SCORE')
                                      .config)
        # The count of the answers
        count = 0
        yes_answers = 0

        # Log the user's responses
        for q_id, answer in json.loads(request.POST['answers']).items():
            # Count he answers to get the percentages later
            if answer == 'True':
                yes_answers += 1
            count += 1

            to_log = TranscriptionLogFeedbackAnswers(
                story_id=story_id,
                user=request.user,
                question_id = q_id,
                answer=answer,
                time=strftime('%Y-%m-%d %H:%M:%S.%s%z', gmtime()),
                session_id=session_id
            )
            to_log.save()

        # Now we need to determine by how much the score should be changed by, the alpha is determined here
        # Get the total number of entries in the ShadowingLogFeedbackAnswers by this user, divide by the number of
        # question and then divide 1 by that number.
        # 1 / (# of user's entries in ShadowingLogFeedbackAnswers) / (# of feedback questions)
        alpha = max(float(TranscriptionConfig.objects.get(name='SCORE_SCALAR_MIN').config),
                    1 / math.log(len((TranscriptionLogFeedbackAnswers.objects.filter(user=request.user))) /
                         len(TranscriptionFeedbackQuestions.objects.all()) + 1))

        # Update the user's stats according to the feedback
        # Make sure they the chars_per_minute does not become higher than the higest chars_per_minute and lower than the
        # lowest chars_per_minute
        percentage = yes_answers/count
        if percentage >= yes_ratio_for_increase and \
                TranscriptionUserStats.objects.get(user=request.user).chars_per_minute < \
                VideoAndSubtitleFilesForTranscription.objects.aggregate(Max('chars_per_minute'))['chars_per_minute__max']:
            # P.objects.filter(username="John Smith").update(accvalue=F("accvalue") + 50)
            TranscriptionUserStats.objects.\
                filter(user=request.user).update(chars_per_minute = F("chars_per_minute") + alpha *
                                                                    change_score_by_constant)
        elif percentage <= no_ratio_for_decrease and \
                TranscriptionUserStats.objects.get(user=request.user).chars_per_minute > \
                VideoAndSubtitleFilesForTranscription.objects.aggregate(Min('chars_per_minute'))['chars_per_minute__min'] :
            TranscriptionUserStats.objects.\
                filter(user=request.user).update(chars_per_minute = F("chars_per_minute") - alpha *
                                                                    change_score_by_constant)

        return JsonResponse({'redirect': '/shadowing/'})