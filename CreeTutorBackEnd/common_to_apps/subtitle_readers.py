"""
File contains a class which aids views that need to process srt files that will be shown to the user.
"""
import re


class SubtitleReader:
    """
    Class was created to aid views that need to process srt files in activities such as transcription and shadowing.
    """
    @staticmethod
    def read_file(file_path, sentences=False):
        """
        Processes the file by calling helper function, return a list of timestamped words
        :param file_path:
        :param sentences:
        :return:
        """
        unindexed_sentences = SubtitleReader.__get_list_of_sentences(file_path)

        segments = SubtitleReader.__get_time_stamped_segments(unindexed_sentences, sentences)
        return segments

    @staticmethod
    def __get_list_of_sentences(file_path):
        """
        # Get a list of all the sentences from file and its time stamps for processing.
        :param location:
        :return:
        """
        # Opening the file
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

    @staticmethod
    def __get_time_stamped_segments(unindexed_sentences, sentences):
        """
        Takes sentences and timestamps, converts them to timestamped segs.
        :param unindexed_sentences:
        :return:
        """
        time_stamped_segments = []
        accumulated_seg_count = 0
        percen = []
        for sentence in unindexed_sentences:
            # Gettings word stats for the sentence, manily len of each segs
            # and total length of the line without white space.
            if not sentences:
                segs = sentence['sen'].split()

                seg_lens = [len(word) for word in segs]
                total_chars = sum(seg_lens)

                # Now getting the percentages for each part of the sentences
                percentages = [float(word_len)/float(total_chars) for word_len in seg_lens]
                percen.append(percentages)

                # Time stamp to milliseconds
                start_time = SubtitleReader.__time_in_milliseconds(sentence['time'][0])
                end_time = SubtitleReader.__time_in_milliseconds(sentence['time'][1])
                delta = end_time - start_time

                # Millisecond timestamps for start and end time of word
                accumulated_time = start_time
                for i in range(0, len(segs)):
                    time_stamped_segments.append([accumulated_seg_count, accumulated_time, delta * percentages[i] +
                                               accumulated_time, segs[i]])
                    accumulated_seg_count += 1
                    accumulated_time += delta * percentages[i]
            else:
                segs = sentence['sen']

                start_time = SubtitleReader.__time_in_milliseconds(sentence['time'][0])
                end_time = SubtitleReader.__time_in_milliseconds(sentence['time'][1])
                accumulated_time = start_time

                time_stamped_segments.append([accumulated_seg_count, accumulated_time, end_time, segs])
                accumulated_seg_count += 1
                accumulated_time = end_time
        return time_stamped_segments

    @staticmethod
    def __time_in_milliseconds(time):
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