from django.shortcuts import render
from django.views import View
from django.views.generic.base import RedirectView
from lettergame.view_helper import *
from time import gmtime, strftime
from django.http import HttpResponse
from django.views.generic.base import TemplateView

# Create your views here.
class Home(TemplateView):
    """
    Class was created to render and return the main page for games.
    """
    template_name = 'home/index.html'