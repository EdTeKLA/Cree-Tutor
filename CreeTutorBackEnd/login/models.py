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

    def __str__(self):
        return self.age_range

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

    def __str__(self):
        return self.level_of_language

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'language_levels'


class LanguagesSpoken(models.Model):
    """
    Store the language that could be spoken, id used as foreign key.
    """
    # The id which will be added into the modified user
    id = models.AutoField(primary_key=True)
    # The age range
    language = models.TextField(unique=True)

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'languages_spoken'


class Gender(models.Model):
    """
    Store the gender of a user.
    """
    # The id which will be added into the modified user
    id = models.AutoField(primary_key=True)
    # The gender of the user
    gender = models.TextField(unique=True)

    def __str__(self):
        return self.gender

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'gender'


class ModifiedUser(AbstractUser):
    """
    A modified user profile, will contain the extra fields that we need.
    """
    age_range = models.ForeignKey(AgeLevels,
                                  on_delete=DO_NOTHING,
                                  null=True)
    gender = models.ForeignKey(Gender,
                               on_delete=DO_NOTHING,
                               null=True,
                               blank=True)
    language_spoken = models.ForeignKey(LanguagesSpoken,
                                        null=True,
                                        on_delete=DO_NOTHING)
    language_level = models.ForeignKey(LanguageLevels,
                                       null=True,
                                       on_delete=DO_NOTHING)
    intake_finished = models.BooleanField(null=False,
                                          blank=False,
                                          default=False)

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
    language_spoken = models.ForeignKey(
        LanguagesSpoken, null=False, on_delete=DO_NOTHING)
    # The fluency level
    language_level = models.ForeignKey(
        LanguageLevels, null=False, on_delete=DO_NOTHING)

    def __str__(self):
        return self.language_spoken, self.language_level

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'user_languages'
