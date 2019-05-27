"""
Files contains functions/classes which turns takes srt files and returns the following statistics:
    - Words per minute
    - Character per minute
    - Word length(mean, median, min, max)
"""
import sys

import django
import os

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
django.setup()
from shadowing.models import *

import re
import numpy as np


class SRTFileStatistics:
    @staticmethod
    def get_srt_stats(file_contents):
        """
        File returns all the statistics generated by this class, this includes:
                - Words per minute
                - Character per minute
                - Word length(mean, median, min, max)

        :param file_contents:
        :return:
        """
        # Read the file and parse it
        words, total_time = SRTFileStatistics.__read_file_and_return_and_returns_words_and_total_time(file_contents)
        # Get length of all the words in words_len
        words_len = [len(word) for word in words]
        # Get all the stats
        stats = {
            'mean': np.mean(words_len),
            'median': np.median(words_len),
            'min': np.min(words_len),
            'max': np.max(words_len),
            'words_per_minute': len(words)/(total_time/60),
            'characters_per_minute': np.sum(words_len)/(total_time/60),
            'number_of_words': len(words),
            'number_of_characters': np.sum(words_len)
        }

        return stats

    @staticmethod
    def __read_file_and_return_and_returns_words_and_total_time(file_contents):
        words = []
        total_time = 0.0

        # Iterating over every line.
        for line in file_contents:
            if re.match('\d{2}:\d{2}:\d{2}[,.]\d{3} --> \d{2}:\d{2}:\d{2}[,]\d{3}', line):
                # Get the time statistics, meaning, take the time and convert it to milliseconds if the line contains
                # a time
                times = line.strip().split(" --> ")
                start_time = SRTFileStatistics.__time_in_seconds(times[0])
                end_time = SRTFileStatistics.__time_in_seconds(times[1])

                total_time += end_time - start_time
            elif re.match('(\d+)\n', line):
                # Ignore the line number
                pass
            elif line != "\n" and line != "":
                # Split the line and add the list of new words to the words list
                words += line.strip().split(" ")

        return words, total_time

    @staticmethod
    def __time_in_seconds(time):
        # Split the time using colons and commas
        time_comps = re.split("[:,]", time)
        # Time to millseconds
        time = (
            int(time_comps[0]) * 3600 + int(time_comps[1]) * 60 + int(time_comps[2])
        )
        return time

class PrepareAdditionalInformationForFile:
    """
    Prepares: name, sub_location and sound_location for insertion in db.
    """
    @staticmethod
    def prepare_additional_information_for_file(file_name, file_stats):
        """
        Takes file names and a file_stats dict and adds name, sub_location and sound_location for insertion in db.
        :param file_name:
        :param file_stats:
        :return:
        """
        # First we need to convert the file name to an actual name
        name = file_name.replace(".srt", "")
        name = name.replace("_", " ")
        name = name.title()
        # Now add the name
        file_stats['name'] = name
        # Now add the sub_location and the sound_location
        file_stats['sub_location'] = "static/srts/" + file_name
        file_stats['sound_location'] = "audio/" + file_name.replace(".srt", "") + ".wav"

        return file_stats

if __name__ == '__main__':
    # Opening the file
    module_dir = os.path.dirname(__file__)  # get current directory
    # Where the files are located
    directory = 'static/srts'
    # Get the path to the directory
    directory_path = os.path.join(module_dir, directory)
    # Will store objects that we need to insert
    objects_to_insert = []

    # Go through every path
    for file in os.listdir(directory_path):
        if not file.startswith('.'):
            # Create the file path
            file_path = directory_path + '/' + file
            print(file_path)
            # Open the file
            file_pointer = open(file_path)
            # Pass it to the methods to get stats
            file_stats = SRTFileStatistics.get_srt_stats(file_pointer)
            dict_for_insert = PrepareAdditionalInformationForFile.prepare_additional_information_for_file(
                file,
                file_stats)
            # Create the object to insert and add to list
            objects_to_insert.append(AudioAndSubtitleFilesForShadowing(**dict_for_insert))

    # Now bulk insert
    AudioAndSubtitleFilesForShadowing.objects.bulk_create(objects_to_insert)