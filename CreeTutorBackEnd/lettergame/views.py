from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.template import loader
from django.forms.models import model_to_dict
from .models import *
import random
import datetime

def index(request):
    # Takes in request and loads the index template

    return render(request, 'lettergame/index.html')


def whichGame(request, game):
    levels = ['learn', 'easy', 'medium', 'hard']
    context = {'game': game, 'levels':levels}
    return render(request, 'lettergame/level.html', context)

def letterGames(request, game, level):
    '''
    Function takes in request.
    If request.method is GET, then function queries letters from the table LetterPair,
    randomizes their order, takes the first five, and passes it into dictionary "context". The sound for the exercise
    is randomly chosen from these chosen 5.
    If request.method id POST, then function takes the post data and stores in it the pairletter_stats table, and Returns
    the context string "double".
    Function returns either dictionary or string or HttpResponse if ERROR.
    '''
    # TODO: rename these. It is not clear
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

    else:
        return HttpResponse('ERROR: game type not adequately identified in view.letterGames')

    if request.method == 'GET':
        context =  getOptions(option, type, level)
        return render(request, 'lettergame/game.html', context)

    elif request.method == 'POST':
        savePostStats(request, option, whichStats, stats, whichDist, level)
        context = getOptions(option, type, level)
        return JsonResponse(context)
    else:
        return HttpResponse('ERROR: request.method not adequately identified in view.letterGames')


def getOptions(option, type, level):
    if level == 'learn':
        num = 1
    elif level == 'easy':
        num = 3
    elif level == 'medium':
        num = 4
    elif level == 'hard':
        num = 5
    options = sorted(option.objects.all(), key=lambda x: random.random())
    options = options[:num]
    sound = random.choice(options)
    if type == 'letter':
        correct = sound.letter
    elif type == 'pair':
        correct = sound.pair
    sound = sound.sound
    lets = list()
    for opt in options:
        if type == 'letter':
            let = opt.letter
        elif type == 'pair':
            let = opt.pair
        lets.append(let)
    context = {
    'letters': lets, 'sound':sound, 'game':'double', 'correct':correct
    }

    return context

def savePostStats(request, option, whichStats, stats, whichDist, level):
    answer = stats()
    user_response = request.POST['user_r']
    correct_response = request.POST['correct_r']
    startTime = request.POST['time_s']
    endTime = request.POST['time_e']
    hoveredArr = request.POST.getlist('arrHov[]')
    dists = request.POST.getlist('distract[]')
    answer.chosen_answer = user_response
    answer.correct_answer = correct_response
    answer.time_started = startTime
    answer.time_ended = endTime
    answer.level = GameLevels.objects.get(name = level)
    answer.save()
    a_id = stats.objects.latest('answer_id')
    for i in hoveredArr:
        j = i.split(',')
        answer_dist = whichStats()
        answer_dist.distracted_by = option.objects.get(pk = j[0])
        answer_dist.answer_id = a_id
        answer_dist.time_hover_start = j[1]
        answer_dist.time_hover_end = j[2]
        answer_dist.save()
    for i in dists:
        distractors = whichDist()
        distractors.distractor = option.objects.get(pk = i)
        distractors.answer_id = a_id
        distractors.save()

    return


def invaderslevel(request):

    return render(request, 'lettergame/invadersmain.html')


def invaders(request, level):
    if level == 'easy':
        num = 3
    elif level == 'medium':
        num = 4
    elif level == 'hard':
        num = 5
    else:
        return HttpResponse('ERROR: variable "level" not passed properly')
    if request.method == 'GET':
        letters = sorted(Alphabet.objects.all().order_by('letter'), key=lambda x: random.random())
        letters = letters[:num]
        context = getOptions(Alphabet, 'letter', level)
        context['level'] = level
        return render(request, 'lettergame/spaceinvadersgame.html', context)
    elif request.method == 'POST':
        letters = sorted(Alphabet.objects.all().order_by('letter'), key=lambda x: random.random())
        letters = letters[:num]
        context = getOptions(Alphabet, 'letter', level)
        context['level'] = level
        return JsonResponse(context)
    else:
        return HttpResponse('ERROR: unknown request passed to views.invaders')


def lemmagame(request):
    if request.method == 'GET':
        return render(request, 'lettergame/lemmagame.html', context)

    elif request.method == 'POST':
        return render(request, 'lettergame/lemmagame.html', context)

    else:
        return HttpResponse('ERROR: request.method was neither GET nor POST')
