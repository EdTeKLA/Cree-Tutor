import time
import random
from random import choice
from time import gmtime, strftime
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from .view_helper import *
from ..models import *
from django.urls import reverse


class BurgerGame(View):

    def post(self, request):

        """
        Saves the data for a player playing the burger game. Returns a JsonResponse
        """
        level = request.POST.get('level')

        id = burgerSession.objects.filter(user=request.user).latest("session_id")
        ts = strftime("%Y-%m-%dT%H:%M:%S%z", gmtime())
        prefix_distractors = request.POST.getlist('prefix_distractors[]')
        suffix_distractors = request.POST.getlist('suffix_distractors[]')
        verb_distractors = request.POST.getlist('verb_distractors[]')
        conjugation_list = request.POST.getlist('conjugation_list[]')
        correct_verb = request.POST.getlist('correct_verb[]')
        on_burger = request.POST.getlist('on_burger[]')

        numberOfCorrect = request.POST.get('numberOfCorrect');

        for i in range(len(on_burger)):
            playerBurg = playerChoseBurgerStats()
            playerBurg.sesh_id = id
            playerBurg.answer = on_burger[i]
            playerBurg.save()

        for i in range(len(prefix_distractors)):
            burgStats = burgerStats()
            burgStats.timeStamp = ts
            burgStats.sesh_id = id
            burgStats.prefixes = prefix_distractors[i]
            burgStats.suffixes = suffix_distractors[i]
            burgStats.verbs = verb_distractors[i]
            burgStats.save()

        for i in range(len(conjugation_list)):
            conjugationBurgs = conjugationBurgerStats()
            conjugationBurgs.sesh_id = id
            conjugationBurgs.conjugation = conjugation_list[i]
            conjugationBurgs.save()

        for i in range(len(correct_verb)):
            verbBurg = verbBurgerStats()
            verbBurg.sesh_id = id
            verbBurg.right_verb = correct_verb[i]
            verbBurg.save()

        context = {'suffixes': [], 'prefixes':[], 'verbs':[], 'correct':[], 'verb':[],'answer':[]}
        context['level'] = level
        context['numberOfCorrect'] = numberOfCorrect
        context = recipe_maker(level)
        return JsonResponse(context)


    def get(self, request):
        new_burger_session = burgerSession()
        new_burger_session.user = request.user
        ts = time.time()
        # new_burger_session.level = level
        new_burger_session.sessionBegin = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        new_burger_session.save()
        id = burgerSession.objects.filter(user=request.user).latest("session_id")
        context = recipe_maker("foo")
        return render(request, 'lettergame/burgergame.html', context)

class BurgerLevelSelect(TemplateView):
    """
    Takes in request and loads the level select template
    """
    template_name = 'lettergame/burger_game_select_level.html'