from django.forms import ModelForm, Form, CharField
from .models import *

#Not sure if a form file is necessary, but just keeping it in case we do need it.

# class SlideForm(ModelForm):
#     """
#     Form mapping to the Slide model
#     """
#     class Meta:
#         model = Slide
#         fields=['level','noun','prefix','suffix']

class LevelForm(Form):
    '''
    Catches the level the user wants to click on
    '''
    level = CharField(label="level", max_length=2)