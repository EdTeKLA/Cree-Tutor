from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
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
    if game == 'single':
        context = singleletter(request)
    elif game == 'double':
        context = letterpair(request)
    else:
        return HttpResponse('ERROR: Game name not passed properly')

    if request.method == 'GET':
        return render(request, 'lettergame/game.html', context)

    elif request.method == 'POST':
        return redirect('lettergame:whichgame', context)

    else:
        return HttpResponse('ERROR: request.method not adequately identified in view.whichgame')

# TODO: The following two functions could probably be condensed into one

def singleletter(request):

    '''
    Function takes in request.
    If request.method is GET, then function queries letters from the table Alphabet,
    randomizes their order, takes the first five, and passes it into dictionary "context". The sound for the exercise
    is randomly chosen from these chosen 5.
    If request.method id POST, then function takes the post data and stores in it the lettergame_stats table, and Returns
    the context string "single".
    Function returns either dictionary or string or HttpResponse if ERROR.
    '''

    if request.method == 'GET':
        letters = sorted(Alphabet.objects.all().order_by('name'), key=lambda x: random.random())
        letters = letters[:5]
        sound = random.choice(letters)
        context = {
        'letters': letters, 'sound':sound, 'game':'single'
        }
        return context
    elif request.method == 'POST':
        user_response = request.POST['user_r']
        correct_response = request.POST['correct_r']

        answer = SingleLetterStats()
        answer.chosen_answer = user_response
        answer.correct_answer = correct_response
        answer.time_answered = datetime.datetime.now()
        answer.save()
        context = 'single'
        return context
    else:
        return HttpResponse('ERROR: request.method not adequately identified in view.singleletter')


def letterpair(request):

    '''
    Function takes in request.
    If request.method is GET, then function queries letters from the table LetterPair,
    randomizes their order, takes the first five, and passes it into dictionary "context". The sound for the exercise
    is randomly chosen from these chosen 5.
    If request.method id POST, then function takes the post data and stores in it the pairletter_stats table, and Returns
    the context string "double".
    Function returns either dictionary or string or HttpResponse if ERROR.
    '''

    if request.method == 'GET':
        letters = sorted(LetterPair.objects.all().order_by('name'), key=lambda x: random.random())
        letters = letters[:5]
        sound = random.choice(letters)
        context = {
        'letters': letters, 'sound':sound, 'game':'double'
        }
        return context
    elif request.method == 'POST':
        user_response = request.POST['user_r']
        correct_response = request.POST['correct_r']

        answer = DoubleLetterStats()
        answer.chosen_answer = user_response
        answer.correct_answer = correct_response
        answer.time_answered = datetime.datetime.now()
        answer.save()
        context = 'double'
        return context
    else:
        return HttpResponse('ERROR: request.method not adequately identified in view.letterpair')

def syl_in_word(request):
    if request.method == 'GET':
        words = sorted(Word.objects.filter(num_syllables = 2), key=lambda x: random.random())
        word = words[0]
        num = random.choice(range(1, word.num_syllables + 1))
        syl = WordSyllable.objects.filter(word_id = word.word_id)

    return HttpResponse(syl[num].vowel)
