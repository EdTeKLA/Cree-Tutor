"""
Files contains code that grabs stats on srt files for audio in the specified folder, then adds the stats and the
location of the files to the db.

This file looks similar to insert_srt_files_stats_and_video_files because it is. Due to the fact they perform the same
function for different files. Main reason they have no been unified and added to DatabaseInsertions is because it the
models for the needed apps refuse to be imported properly when the files are running.
"""
import sys
import django
import os

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
django.setup()


from shadowing.models import *
from DatabaseInsertions.get_stats_on_srt_files import *

# Only execute if this is the called file, if file imported, will not execute

if __name__ == '__main__':
    # Opening the file
    module_dir = os.path.dirname(__file__)  # get current directory
    # Where the files are located
    directory = 'static/srts'
    # Get the path to the directory
    directory_path = os.path.join(module_dir, directory)
    # Will store objects that we need to insert

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
                file_stats,
                "wav")

            # Create the object to insert and add to list
            AudioAndSubtitleFilesForShadowing.objects.get_or_create(dict_for_insert, name=dict_for_insert['name'])