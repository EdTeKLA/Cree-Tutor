import sys

import django
import os

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CreeTutorBackEnd.CreeTutorBackEnd.settings")
django.setup()

from login.models import AgeLevels


def insert_age_range():
    """
    Inserts a date range into the right table
    :return:
    """
    # All the ranges
    ranges = [
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

    # Save the ranges
    for range in ranges:
        # Put dicts into the database if they don't exist
        range_dict = {"age_range": range}
        AgeLevels.objects.update_or_create(range_dict, age_range=range)


if __name__ == '__main__':
    insert_age_range()