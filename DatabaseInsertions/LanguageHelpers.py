"""
File was created to hold classes that will help with data insertion by generating any additonal data needed linked to
language.
"""
import re


class LanguageHelpers:
    """
    Class contains methods to generate data for insertion into db.
    """

    @staticmethod
    def count_syllables(word):
        """
        Method takes in word string and counts the number of syllables.
        Returns int, number of syllables
        Ref: https://stackoverflow.com/questions/46759492/syllable-count-in-python
        :param self:
        :return:
        """
        # TODO: Consider whether 'ew' counts as two syllables

        count = 0
        vowels = 'aeioâîô'
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if count == 0:
            count += 1

        return count

    @staticmethod
    def type_of_letter(letter):
        """
        Returns which type of letter is passed in. Returns vowel, semivowel, semivowel.
        :param letter:
        :return:
        """
        # Types of words
        vowels = ['a', 'e', 'i', 'o']
        semivowels = ['y', 'w']

        if letter in vowels:
            return 'vowel'
        elif letter in semivowels:
            return 'semivowel'
        else:
            return

    @staticmethod
    def split_pair_into_letters(pair):
        """
        Takes a pair, breaks it up and returns 2 letters.
        :param pair:
        :return:
        """
        first = None
        second = None

        if len(pair) == 2:
            first = pair[0]
            second = pair[1]
        else:
            # if the accent (\W) is on the first letter
            m = re.match('(\w\W)(\w)', pair)
            # if the accent (\W) is on the second letter
            n = re.match('(\w)(\w\W)', pair)

            if m is not None:
                first = m.group(1)
                second = m.group(2)

            elif n is not None:
                first = n.group(1)
                second = n.group(2)

        return first, second

    @staticmethod
    def difference_between_words(a, b):
        """
        Method returns the number of letters that differ between a and b, used for minimal pairs.
        :param a:
        :param b:
        :return:
        """
        a = a.lower()
        b = b.lower()
        if a == b:
            return 100
        zipped = zip(a, b)  # give list of tuples (of letters at each index)
        difference = sum(1 for e in zipped if e[0] != e[1])  # count tuples with non matching elements
        difference = difference + abs(len(a) - len(b))
        return difference