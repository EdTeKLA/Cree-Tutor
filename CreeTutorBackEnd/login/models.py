import django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import DO_NOTHING, CASCADE
from django.urls import reverse

class AgeLevels(models.Model):
    """
    Store the age levels of a person.
    """
    # The id which will be added into the modified user
    id = models.AutoField(primary_key=True)

    # The age range
    age_range = models.TextField(unique=True)

    def __str__(self):
        # Used when you call Age levels in the front end to display the values stored in
        # the database, also capitalized for formatting
        return self.age_range.capitalize()

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
    language_level = models.TextField(unique=True)

    def __str__(self):
        return self.language_level.capitalize()

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

    def __str__(self):
        return self.language.capitalize()
    
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
        return self.gender.capitalize()

    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'gender'


class ModifiedUser(AbstractUser):
    """
    A modified user profile, will contain the extra fields that we need.
    """
    # Emails and usernames should be allowed to be null because we need to be able to disable accounts and 
    # wipe the content stored there so that users can create new accounts using previously used emails
    email = models.EmailField(blank=True, 
                                null=True,
                                max_length=254, 
                                verbose_name='email address')
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, 
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', 
                                max_length=150, 
                                unique=True, 
                                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], 
                                verbose_name='username',
                                null=True)
    age_range = models.ForeignKey(AgeLevels,
                                  on_delete=DO_NOTHING,
                                  null=True, 
                                  blank=False)
    gender = models.ForeignKey(Gender,
                               on_delete=DO_NOTHING,
                               null=True,
                               blank=False)
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

    def __str__(self):
        return "<Modified User object: %s"%self.username

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
    def get_absolute_url(self):
        return reverse('login:profile-language-edit', kwargs={'pk': self.pk})
    class Meta:
        app_label = 'login'
        managed = True
        db_table = 'user_languages'