import math
from time import gmtime, strftime

import json
import re
import os
from django.shortcuts import render
from django.views import View
from shadowing.models import AudioAndSubtitleFilesForShadowing, ShadowingFeedbackQuestions, ShadowingLogActions, \
    ShadowingUserStats, ShadowingLogFeedbackAnswers, ShadowingConfig
from django.http import HttpResponseNotFound, JsonResponse
from django.db.models import Min, F, Max


class Index(View):
    """
    Renders and shows the list of stories in the db.
    """
    def get(self, request):
        """
        Uses a sliding window to show stories that might be relevent to this user.
        :param request:
        :return:
        """
        sliding_window_size = float(ShadowingConfig.objects.get(name='SLIDING_WINDOW_SIZE_FOR_FETCH').config)
        min_number_of_stories = float(ShadowingConfig.objects.get(name='MIN_NUMBER_OF_STORIES').config)
        # First we try to get the statistics of the user that is request the page
        try:
            user_stats = ShadowingUserStats.objects.get(user_id = request.user.id)
        except ShadowingUserStats.DoesNotExist:
            user_stats = ShadowingUserStats(
                user=request.user,
                chars_per_minute=AudioAndSubtitleFilesForShadowing.objects.aggregate(
                    Min('chars_per_minute'))['chars_per_minute__min']
            )

            user_stats.save()

        min_chars_per_minute = user_stats.chars_per_minute - sliding_window_size
        max_chars_per_minute = user_stats.chars_per_minute + sliding_window_size

        # Now filtering the stories according to the window size and
        all_stories = []
        while len(all_stories) < min_number_of_stories:
            all_stories = AudioAndSubtitleFilesForShadowing.objects.filter(
                chars_per_minute__range=(min_chars_per_minute, max_chars_per_minute)
            )

            min_chars_per_minute -= sliding_window_size
            max_chars_per_minute += sliding_window_size

        context = {"all_stories": all_stories}

        return render(request, 'shadowing/index.html', context)


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
            context = {"audio_file_loc": story_info.sound_location,
                       "audio_transcript_list": self.__read_file(story_info.sub_location),
                       "story_id": story_index}
            return render(request, 'shadowing/story.html', context)
        except AudioAndSubtitleFilesForShadowing.DoesNotExist:
            return HttpResponseNotFound("Page Not Found")

    def __read_file(self, location):
        """
        Processes the file by calling helper function, return a list of timestamped words
        :param location:
        :return:
        """
        unindexed_sentences = self.__get_list_of_sentences(location)
        words = self.__get_time_stamped_words(unindexed_sentences)
        return words

    def __get_list_of_sentences(self, location):
        """
        # Get a list of all the sentences from file and its time stamps for processing.
        :param location:
        :return:
        """
        # Opening the file
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, location)
        f = open(file_path)

        sentences = []
        current_sentence = {}

        # Iterating over every line.
        for line in f:
            # Remove any white space on the right, this is mainly for \n
            line.rstrip()
            # Try to match the sentence to a timestamp format, a number or non
            # empty line
            # If empty line, finished, move on to next set
            # DO NOT CHANGE THE ORDER OF FIRST TWO!!!
            if re.match('\d{2}:\d{2}:\d{2}[,.]\d{3} --> \d{2}:\d{2}:\d{2}[,]\d{3}', line):
                current_sentence['time'] = line.strip().split(" --> ")
            elif re.match('(\d+)\n', line):
                current_sentence['ln'] = line.strip()
            elif line != "\n" and line != "":
                if 'sen' in current_sentence:
                    current_sentence['sen'] += (" " + line.strip())
                else:
                    current_sentence['sen'] = line.strip()
            else:
                sentences.append(current_sentence)
                current_sentence = {}

        return sentences

    def __get_time_stamped_words(self, unindexed_sentences):
        """
        Takes sentences and timestamps, converts them to timestamped words.
        :param unindexed_sentences:
        :return:
        """
        time_stamped_words = []
        accumulated_word_count = 0
        percen = []
        for sentence in unindexed_sentences:
            # Gettings word stats for the sentence, manily len of each words
            # and total length of the line without white space.
            words = sentence['sen'].split()

            words_lens = [len(word) for word in words]
            total_chars = sum(words_lens)

            # Now getting the percentages for each part of the sentences
            percentages = [float(word_len)/float(total_chars) for word_len in words_lens]
            percen.append(percentages)

            # Time stamp to milliseconds
            start_time = self.__time_in_milliseconds(sentence['time'][0])
            end_time = self.__time_in_milliseconds(sentence['time'][1])
            delta = end_time - start_time

            # Millisecond timestamps for start and end time of word
            accumulated_time = start_time
            for i in range(0, len(words)):
                time_stamped_words.append([accumulated_word_count, accumulated_time, delta * percentages[i] + accumulated_time, words[i]])
                accumulated_word_count += 1
                accumulated_time += delta * percentages[i]
        return time_stamped_words

    def __time_in_milliseconds(self, time):
        """
        Helper function to convert time to milliseconds.
        :param time:
        :return:
        """
        # Split the time using colons and commas
        time_comps = re.split("[:,]", time)
        # Time to millseconds
        time = (
            int(time_comps[0]) * 3600 + int(time_comps[1]) * 60 + int(time_comps[2])
        ) * 1000 + int(time_comps[3])
        return time


class ShadowingFeedBack(View):
    """
    Renders the answers.

    Saves the logs for how the person answered and updates the values of what where they score is.
    """
    def get(self, request, story_id):
        """
        Gets all the questions from the database for shadowing questions and puts it into a context to show the user.
        :param request:
        :param story_id:
        :return:
        """
        questions = ShadowingFeedbackQuestions.objects.all()

        # Create the context and render
        context = { "story_id": story_id, "questions": questions }
        return render(request, 'shadowing/feedback.html', context)

    def post(self, request, story_id):
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
    def post(self, request, story_id, action, time):
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
                time=strftime('%Y-%m-%d %H:%M:%S.%s%z', gmtime())
            )

            log.save()
            return JsonResponse({"status": "success"})
        except:
            return JsonResponse({"status": "error"})