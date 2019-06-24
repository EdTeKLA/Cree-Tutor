from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import DO_NOTHING, CASCADE


class AgeLevels(models.Model):
    """
    Store the age levels of a person.
    """
    # The id which will be added into the modified user
    id = models.AutoField(primary_key=True)
    # The age range
    age_range = models.TextField(unique=True)

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'age_levels'


class LanguageLevels(models.Model):
    """
    The level at which the person speaks the language.
    """
    id = models.AutoField(primary_key=True)
    # The level of the language
    level_of_language = models.TextField(unique=True)

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'language_levels'


class LanguagesSpoken(models.Model):
    """
    Store the age levels of a person.
    """
    # The id which will be added into the modified user
    id = models.AutoField(primary_key=True)
    # The age range
    language = models.TextField(unique=True)

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'languages_spoken'


class ModifiedUser(AbstractUser):
    """
    A modified user profile, will contain the extra fields that we need.
    """
    age_level = models.ForeignKey(AgeLevels, on_delete=DO_NOTHING, null=True)
    intake_finished = models.BooleanField(null=False, blank=False, default=False)

    def __init__(self, *args, **kwargs):
        """
        Adds the extra fields
        :param args:
        :param kwargs:
        """
        super(ModifiedUser, self).__init__(*args, **kwargs)

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'modified_user'


class UserLanguages(models.Model):
    """
    The languages the user speaks with the level.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(ModifiedUser, on_delete=CASCADE)
    # The language the user speaks
    language_spoken = models.ForeignKey(LanguagesSpoken, null=False, on_delete=DO_NOTHING)
    # The fluency level
    level_of_language = models.ForeignKey(LanguageLevels, null=False, on_delete=DO_NOTHING)

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'user_languages'