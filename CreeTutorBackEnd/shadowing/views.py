import re
import os
from django.shortcuts import render
from django.views import View
from shadowing.models import AudioAndSubtitleFilesForShadowing
from django.http import HttpResponse, HttpResponseNotFound


class Index(View):
    """
    """
    def get(self, request):
        all_stories = AudioAndSubtitleFilesForShadowing.objects.all()
        context = { "all_stories": all_stories}

        return render(request, 'shadowing/index.html', context)


class Shadowing(View):
    """
    """
    def get(self, request, story_index):
        try:
            story_info = AudioAndSubtitleFilesForShadowing.objects.get(id=story_index)
            context = {"audio_file_loc": story_info.sound_location,
                       "audio_transcript_list": self.__read_file(story_info.sub_location)}
            return render(request, 'shadowing/story.html', context)
        except AudioAndSubtitleFilesForShadowing.DoesNotExist:
            return HttpResponseNotFound("Page Not Found")

    def __read_file(self, location):
        unindexed_sentences = self.__get_list_of_sentences(location)
        words = self.__get_time_stamped_words(unindexed_sentences)
        return words

    def __get_list_of_sentences(self, location):
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
        time_stamped_words = []
        accumulated_word_count = 0
        percen = []
        for sentence in unindexed_sentences:
            # Gettings word stats for the sentence, manily len of each words
            # and total length of the line without white space.
            words = sentence['sen'].split()

            words_lens = [len(word) for word in words]
            total_chars = sum(words_lens)
            print(words_lens)

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
        # Split the time using colons and commas
        time_comps = re.split("[:,]", time)
        # Time to millseconds
        time = (
            int(time_comps[0]) * 3600 + int(time_comps[1]) * 60 + int(time_comps[2])
        ) * 1000 + int(time_comps[3])
        return time
