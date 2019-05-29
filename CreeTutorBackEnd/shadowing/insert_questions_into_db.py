import sys

import django
import os

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.settings")
django.setup()

from shadowing.models import ShadowingFeedbackQuestions


def insert_questions_into_db():
    """
    Function was created to bulk insert questions into the database
    :return:
    """
    answer_could = ["I could", "I could not"]
    answer_yes = ["Yes", "No"]

    questions = [
        ["I could speak all the words aloud", answer_could],
        ["I could pronounce all of the words correctly", answer_could],
        ["I could keep up with the reader", answer_could],
        ["I could understand all of the text", answer_could],
        ["I could easily complete the activity", answer_could],
    ]

    question_objs = []

    for question in questions:
        obj = ShadowingFeedbackQuestions(
            question=question[0],
            yes_answer=question[1][0],
            no_answer=question[1][1],
        )

        question_objs.append(obj)

    ShadowingFeedbackQuestions.objects.bulk_create(question_objs)

if __name__ == '__main__':
    insert_questions_into_db()