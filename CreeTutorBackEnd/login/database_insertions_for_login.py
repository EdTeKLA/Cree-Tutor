"""
File contains all the methods that insert data into tables for the login app.
"""
import sys

import django
import os

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.CreeTutorBackEnd.settings")
django.setup()

from login.models import AgeLevels


def insert_age_ranges_into_db():
    """
    Inserts the age ranges for users into the db.
    :return:
    """
    age_levels = [
        "12 or younger",
        "12-18",
        "19-29",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
        "70 or older",
        "Prefer not to answer",
    ]

    # Go through all the age ranges
    for age_level in age_levels:
        age_level = AgeLevels(age_range=age_level)
        age_level.save()


if __name__ == '__main__':
    insert_age_ranges_into_db()