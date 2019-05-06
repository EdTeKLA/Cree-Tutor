from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from lettergame.view_helper import *
from time import gmtime, strftime
from django.http import HttpResponse

# Create your views here.
class Home(View):
    """
    Class was created to render and return the main page for games.
    """
    template_name = 'home/index.html'
