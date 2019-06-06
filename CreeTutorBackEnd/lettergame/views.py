from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.template import loader
from django.forms.models import model_to_dict
from .models import *
import random
import datetime
from django.db.models import Q
import time
from django.views import View
from django.views.generic.base import TemplateView
from lettergame.view_helper import *
from time import gmtime, strftime


class WhichGame(View):
    """
    Renders the page to ask the user which level he/she would like to play with.
    """
    def get(self, request, game):
        """
        Takes a game variable and creates other variables that are needed to
        render level.html
        """
        levels = []

        levels = ['learn', 'easy', 'medium', 'hard']
        context = {'game': game, 'levels':levels}

        return render(request, 'lettergame/level.html', context)

class LetterGames(View):
    """
    Function takes in request, game, and level parameters to determine the game (single/double) and level (learn/easy/...).
    It them renders the game or saves the stats depending on the type of request.
    """
    def get(self, request, game, level):
        """
        Method passes appropriate parameters to getOptions and then renders the game.html template.
        """
        # Get the options to render the context
        option, whichStats, type, stats, whichDist = self.__prepare_options(request, game, level)

        # get new options for game
        context =  getOptions(option, type, level)
        return render(request, 'lettergame/game.html', context)

    def post(self, request, game, level):
        """
        Saves the data that has been passed in and returns a JsonResponse
        """
        # Get the options needed to save the data and prepare the Json response
        option, whichStats, type, stats, whichDist = self.__prepare_options(request, game, level)

        # Save stats, then get new options for next question
        savePostStats(request, option, whichStats, stats, whichDist, level)
        context = getOptions(option, type, level)

        return JsonResponse(context)

    def __prepare_options(self, request, game, level):
        """
        Returns a list of variables that will be used to render contexts by get/post
        """
        if game == 'double':
            option = LetterPair
            whichStats = DLSDistractedBy
            type = 'pair'
            stats = DoubleLetterStats
            whichDist = DLSDistractors
        elif game == 'single':
            option = Alphabet
            type = 'letter'
            stats = SingleLetterStats
            whichStats = SLSDistractedBy
            whichDist = SLSDistractors

        return option, whichStats, type, stats, whichDist

class InvadersLevel(TemplateView):
    """
    Takes in request and loads the invadersmain template
    """
    template_name = 'lettergame/invadersmain.html'

class Invaders(View):
    """
    Serves up the Invaders game and saves any data that is sent in a POST request
    """

    def get(self, request, level):
        """
        Returns an invaders game level. Returns a HttpResponse
        """
        new_invaders_session = invadersSession()
        new_invaders_session.user = request.user
        ts = time.time()
        new_invaders_session.sessionBegin = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        new_invaders_session.level = level
        new_invaders_session.save()
        id = invadersSession.objects.filter(user=request.user).latest("session_id")
        context = inv_distractors(level, set(), id)
        context['level'] = level
        return render(request, 'lettergame/spaceinvadersgame.html', context)

    def post(self, request, level):
        """
        Saves the data for a player playing the invader game. Returns a JsonResponse
        """
        num = self.__get_user_and_level_number(request, level)

        onScreen = set()
        id = invadersSession.objects.filter(user=request.user).latest("session_id")
        ts = strftime('%Y-%m-%d %H:%M:%S.%s%z', gmtime())
        letters = request.POST.getlist('onScreenLetters[]')
        positions = request.POST.getlist('positions[]')
        hits = request.POST.getlist('hit[]')
        correct = request.POST['correct']
        for i in range(len(letters)):
            invStats = invadersStats()
            invStats.timeStamp = ts
            invStats.sesh_id = id
            invStats.correct = correct
            invStats.screen_position = positions[i]
            invStats.letter = letters[i]
            invStats.hit_or_left = hits[i]
            if hits[i] == "false":
                onScreen.add(letters[i])
            else:
                if letters[i] == correct:
                    userCorrect = invadersUserCorrect()
                    userCorrect.sesh_id = id
                    userCorrect.letter = letters[i]
                    userCorrect.save()
            invStats.save()
        more_inv = request.POST['populate']

        context = {'letters': [], 'sound':"", 'game':'single', 'correct':'', 'level':level}

        if int(request.POST['numInvadersLeft']) < num +1 and more_inv == "true":
            context = inv_distractors(level, onScreen, id)
            context['level'] = level

        return JsonResponse(context)

    def __get_user_and_level_number(self, request, level):
        """
        Get the user and the level number
        """
        # Check the level the person is playing at.
        if level == 'easy':
            num = 3
        elif level == 'medium':
            num = 4
        elif level == 'hard':
            num = 4
        else:
            num = None

        return num
