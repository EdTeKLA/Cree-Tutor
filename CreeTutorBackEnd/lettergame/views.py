from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.template import loader
from django.forms.models import model_to_dict
from .models import Alphabet, SingleLetterStats, LetterPair, DoubleLetterStats, Word, WordSyllable
import random
import datetime

def index(request):
    # Takes in request and loads the index template

    return render(request, 'lettergame/index.html')

def whichgame(request, game):

    '''
    Function takes in request and game name. If game is "single", then the client
    has requested to play the single letter game, and similarly for game == "double".
    Function passes these requests to either singleletter or letterpair, or returns an
    error via HttpResponse.
    Returns type HttpResponse.
    '''

    context = None
    if game == 'single' or game == 'double':
        context = letterGames(request, game)
    else:
        return HttpResponse('ERROR: Game name not passed properly')

    if request.method == 'GET':
        return render(request, 'lettergame/game.html', context)
    elif request.method == 'POST':
        return JsonResponse(context)
    else:
        return HttpResponse('ERROR: request.method not adequately identified in view.whichgame.')


def letterGames(request, game):
    '''
    Function takes in request.
    If request.method is GET, then function queries letters from the table LetterPair,
    randomizes their order, takes the first five, and passes it into dictionary "context". The sound for the exercise
    is randomly chosen from these chosen 5.
    If request.method id POST, then function takes the post data and stores in it the pairletter_stats table, and Returns
    the context string "double".
    Function returns either dictionary or string or HttpResponse if ERROR.
    '''
    if game == 'double':
        options = sorted(LetterPair.objects.all().order_by('pair'), key=lambda x: random.random())
        type = 'pair'
        answer = DoubleLetterStats()

    elif game == 'single':
        options = letters = sorted(Alphabet.objects.all().order_by('letter'), key=lambda x: random.random())
        type = 'letter'
        answer = SingleLetterStats()

    else:
        return HttpResponse('ERROR: game type not adequately identified in view.letterGames')

    if request.method == 'GET':
        return getOptions(options, type)

    elif request.method == 'POST':
        user_response = request.POST['user_r']
        correct_response = request.POST['correct_r']
        time_spent = request.POST['time_s']
        answer.chosen_answer = user_response
        answer.correct_answer = correct_response
        answer.time_answered = datetime.datetime.now()
        answer.time_spent = time_spent
        answer.save()
        return getOptions(options, type)

    else:
        return HttpResponse('ERROR: request.method not adequately identified in view.letterGames')

def getOptions(options, type):

    options = options[:5]
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

def syl_in_word(request):
    if request.method == 'GET':
        words = sorted(Word.objects.filter(num_syllables = 2), key=lambda x: random.random())
        word = words[0]
        num = random.choice(range(1, word.num_syllables + 1))
        syl = WordSyllable.objects.filter(word_id = word.word_id)

    return HttpResponse(syl[num].vowel)

def invaderslevel(request):

    return render(request, 'lettergame/invadersmain.html')

def invaders(request, level):
    if level == 'easy':
        num = 3
    elif level == 'med':
        num = 4
    elif level == 'hard':
        num = 5
    else:
        return HttpResponse('ERROR: variable "level" not passed properly')
    if request.method == 'GET':
        letters = sorted(Alphabet.objects.all().order_by('letter'), key=lambda x: random.random())
        letters = letters[:num]
        sound = random.choice(letters)
        sound.name = sound.letter
        for letter in letters:
            letter.name = letter.letter
        context = {
        'letters': letters, 'sound':sound, 'level':level
        }
        return render(request, 'lettergame/spaceinvadersgame.html', context)

    else: 
        return HttpResponse('ERROR: POST request passed to views.invaders')