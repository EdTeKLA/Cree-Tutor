import sys

import django
import os

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
django.setup()

from transcription.models import TranscriptionFeedbackQuestions


def insert_questions_into_db():
    """
    Function was created to bulk insert questions into the database
    :return:
    """
    # answer_could = ["I could", "I could not"]
    answer_yes = ["Yes", "No"]

    questions = [
        ["Question 1", answer_yes],
        ["Question 2", answer_yes],
        ["Question 3", answer_yes],
        ["Question 4", answer_yes],
        ["Question 5", answer_yes],
    ]

    for question in questions:
        TranscriptionFeedbackQuestions.objects.get_or_create(
            question=question[0],
            yes_answer=question[1][0],
            no_answer=question[1][1],
        )

if __name__ == '__main__':
    insert_questions_into_db()