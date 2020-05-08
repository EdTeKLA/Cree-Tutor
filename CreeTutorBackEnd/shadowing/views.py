import math
from time import gmtime, strftime
import uuid
import os

import json
from django.shortcuts import render
from django.views import View
from shadowing.models import AudioAndSubtitleFilesForShadowing, ShadowingFeedbackQuestions, ShadowingLogActions, \
    ShadowingUserStats, ShadowingLogFeedbackAnswers, ShadowingConfig
from django.http import HttpResponseNotFound, JsonResponse
from django.db.models import Min, F, Max

from common_to_apps.view_specialized_for_character_per_minute_activities\
    import IndexForListOfChoicesInWindowForUserStatsForCharacterPerMinuteOrSubclasses
from common_to_apps.subtitle_readers import SubtitleReader


class Index(IndexForListOfChoicesInWindowForUserStatsForCharacterPerMinuteOrSubclasses):
    """
    Renders and shows the list of stories in the db.
    """
    config_class = ShadowingConfig
    user_stats_class = ShadowingUserStats
    media_table_to_filter_from = AudioAndSubtitleFilesForShadowing
    template_to_render = 'shadowing/index.html'
    size_of_window_config = 'SLIDING_WINDOW_SIZE_FOR_FETCH'
    min_number_of_choices_config = 'MIN_NUMBER_OF_CHOICES'


class Shadowing(View):
    """
    Class was created to render the shadowing page where the story is displayed.
    """
    def get(self, request, story_index):
        """
        Gets the requested story, processes the text and renders the story tempalte
        :param request:
        :param story_index:
        :return:
        """
        try:
            story_info = AudioAndSubtitleFilesForShadowing.objects.get(id=story_index)

            module_dir = os.path.dirname(__file__)  # get current directory
            file_path = os.path.join(module_dir, story_info.sub_location)
            transcript = SubtitleReader.read_file(file_path)

            context = {"audio_file_loc": story_info.media_location,
                       "audio_transcript_list": transcript,
                       "story_id": story_index,
                       "session_id": uuid.uuid4()}
            return render(request, 'shadowing/story.html', context)
        except AudioAndSubtitleFilesForShadowing.DoesNotExist:
            return HttpResponseNotFound("Page Not Found")


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
        questions = ShadowingFeedbackQuestions.objects.all()

        # Create the context and render
        context = { "story_id": story_id, "questions": questions, "session_id":session_id }
        return render(request, 'shadowing/feedback.html', context)

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
        change_score_by_constant = float(ShadowingConfig.objects.get(name='CHANGE_SCORE_BY').config)
        # Variables hold the number of question that will change the person's score up or down
        yes_ratio_for_increase = float(ShadowingConfig.objects.get(name='FEEDBACK_RATIO_TO_INCREASE_SCORE').config)
        no_ratio_for_decrease = float(ShadowingConfig.objects.get(name='FEEDBACK_RATIO_TO_DECREASE_SCORE').config)
        # The count of the answers
        count = 0
        yes_answers = 0

        # Log the user's responses
        for q_id, answer in json.loads(request.POST['answers']).items():
            # Count he answers to get the percentages later
            if answer == 'True':
                yes_answers += 1
            count += 1

            to_log = ShadowingLogFeedbackAnswers(
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
        alpha = max(float(ShadowingConfig.objects.get(name='SCORE_SCALAR_MIN').config),
                    1 / math.log(len((ShadowingLogFeedbackAnswers.objects.filter(user=request.user))) /
                         len(ShadowingFeedbackQuestions.objects.all()) + 1))

        # Update the user's stats according to the feedback
        # Make sure they the chars_per_minute does not become higher than the higest chars_per_minute and lower than the
        # lowest chars_per_minute
        percentage = yes_answers/count
        if percentage >= yes_ratio_for_increase and \
                ShadowingUserStats.objects.get(user=request.user).chars_per_minute < \
                AudioAndSubtitleFilesForShadowing.objects.aggregate(Max('chars_per_minute'))['chars_per_minute__max']:
            # P.objects.filter(username="John Smith").update(accvalue=F("accvalue") + 50)
            ShadowingUserStats.objects.\
                filter(user=request.user).update(chars_per_minute = F("chars_per_minute") + alpha *
                                                                    change_score_by_constant)
        elif percentage <= no_ratio_for_decrease and \
                ShadowingUserStats.objects.get(user=request.user).chars_per_minute > \
                AudioAndSubtitleFilesForShadowing.objects.aggregate(Min('chars_per_minute'))['chars_per_minute__min'] :
            ShadowingUserStats.objects.\
                filter(user=request.user).update(chars_per_minute = F("chars_per_minute") - alpha *
                                                                    change_score_by_constant)

        return JsonResponse({'redirect': '/shadowing/'})


class ShadowingLogging(View):
    """
    Only takes post request. Logs the information for the shadowing questions.
    """
    def post(self, request, story_id, action, time, session_id):
        """
        Logs the information for shadowing. This includes the information in ShadowingLogStorySelection model.
        :param request:
        :param story_id:
        :param action:
        :param time:
        :return:
        """
        # Attempts to log the action and returns the status
        try:
            log = ShadowingLogActions(
                user=request.user,
                story_id=story_id,
                action=action,
                story_time=time,
                time=strftime('%Y-%m-%d %H:%M:%S.%s%z', gmtime()),
                session_id=session_id
            )

            log.save()
            return JsonResponse({"status": "success"})
        except:
            return JsonResponse({"status": "error"})