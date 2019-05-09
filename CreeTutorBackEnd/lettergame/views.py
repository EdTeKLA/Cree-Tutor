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

def index(request):
    # Takes in request and loads the index template
    return render(request, 'lettergame/index.html')

def handleOptions(function, request):
    function(request)

def whichGame(request, game):
    '''
    Function takes in request (presumably GET request) and game variable.
    Sets up appropriate context to render the level.html template.
    Returns the render of the level.html template.
    '''

    levels = ['learn', 'easy', 'medium', 'hard']
    context = {'game': game, 'levels':levels, 'gameType':'letterGames'}

    return render(request, 'lettergame/level.html', context)


def letterGames(request, game, level):
    '''
    Function takes in request, game, and level parameters to determine the game (single/double) and level (learn/easy/...)
    If request.method is GET, function passes appropriate parameters to getOptions and then renders the game.html template.
    If request.method id POST, function passes appropriate parameters to first savePostStats to save the data post-ed from client
    side, then passes appropriate parameters to getOptions and returns a json response back to client side.
    Function returns either an HttpResponse or a JsonResponse.
    '''

    # Depending on the game, set appropriate variables to be passed to getOptions and/or savePostStats
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

    # For debugging -- To be removed before deployment
    else:
        return HttpResponse('ERROR: game type not adequately identified in view.letterGames')

    if request.method == 'GET':
        # get new options for game
        context =  getOptions(option, type, level)
        return render(request, 'lettergame/game.html', context)

    elif request.method == 'POST':
        # save posted stats, then get new options for next question
        savePostStats(request, option, whichStats, stats, whichDist, level)
        context = getOptions(option, type, level)
        return JsonResponse(context)

    # For debugging -- To be removed before deployment
    else:
        return HttpResponse('ERROR: request.method not adequately identified in view.letterGames')


def getOptions(option, type, level):
    '''
    Function retrieves options for both single and double letter game. How many options depends on level.
    Currently picks distractors at random.
    Return dictionary "context" containing information on the level, options, correct answer, and sound path.
    '''
    # Determine the number of options for level
    if level == 'learn':
        num = 1
    elif level == 'easy':
        num = 3
    elif level == 'medium':
        num = 4
    elif level == 'hard':
        num = 5

    # Extract options from appropriate model and randomize them
    options = sorted(option.objects.all(), key=lambda x: random.random())
    options = options[:num]
    sound = random.choice(options)
    # Front end javascript does not jive well with Django model objects, and so we pass instead specific strings instead
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
    '''
    Function takes in parameters about the post request (request), the models the
    data should be submitted to, and the data that needs submitting
    Submits data and returns nothing
    '''

    answer = stats() # stats is either the class SingleLetterStats or DoubleLetterStats
    # retreive posted data
    user_response = request.POST['user_r']
    correct_response = request.POST['correct_r']
    startTime = request.POST['time_s']
    endTime = request.POST['time_e']
    hoveredArr = request.POST.getlist('arrHov[]')
    dists = request.POST.getlist('distract[]')
    #submit first to _LetterStats
    answer.chosen_answer = user_response
    answer.correct_answer = correct_response
    answer.time_started = startTime
    answer.time_ended = endTime
    answer.level = GameLevels.objects.get(name = level)
    answer.save()
    # For both games, the distractedby and distractors table depend on the answer_id from the _LetterStats submission
    a_id = stats.objects.latest('answer_id')
    # Insert data relating to options user hovered over
    for i in hoveredArr:
        j = i.split(',')
        answer_dist = whichStats()
        answer_dist.distracted_by = option.objects.get(pk = j[0])
        answer_dist.answer_id = a_id
        answer_dist.time_hover_start = j[1]
        answer_dist.time_hover_end = j[2]
        answer_dist.save()
    # Insert the distractors
    for i in dists:
        distractors = whichDist()
        distractors.distractor = option.objects.get(pk = i)
        distractors.answer_id = a_id
        distractors.save()

    return


def invadersgame(request):
    # Takes in request and loads the invadersmain template
    game = ''
    levels = ['single', 'double', 'minimalpair', 'word']
    context = {'game': game, 'levels':levels, 'gameType':'invaderslevel'}

    return render(request, 'lettergame/invadersgame.html', context)

    # return render(request, 'lettergame/invadersmain.html')

def invaderslevel(request, game, level):

    context = {'game':game}

    return render(request, 'lettergame/invadersmain.html', context)

def invaders(request, level):
    '''
    Function takes in request (GET or POST) and which level the user wishes to play the invaders game at ("easy", "medium", "hard").
    Currently takes __ numbers of options from the Alphabet table at random. Will be updated to follow the same procedure and use the same functions as letterGames.
    Returns a JsonResponse or HttpResponse.
    '''

    user = None
    if request.user.is_authenticated:
        user = request.user

    if level == 'easy':
        num = 3
    elif level == 'medium':
        num = 4
    elif level == 'hard':
        num = 4
    else:
        return HttpResponse('ERROR: variable "level" not passed properly')

    if request.method == 'GET':

        new_invaders_session = invadersSession()
        new_invaders_session.user = user
        ts = time.time()
        new_invaders_session.sessionBegin = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        new_invaders_session.level = level
        new_invaders_session.save()
        id = invadersSession.objects.filter(user=user).latest("session_id")
        context = inv_distractors(level, set(), id)
        context['level'] = level
        return render(request, 'lettergame/spaceinvadersgame.html', context)

    elif request.method == 'POST':
        onScreen = set()
        id = invadersSession.objects.filter(user=user).latest("session_id")
        ts = time.time()
        ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
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


    else:
        # For debugging -- To be removed before deployment
        return HttpResponse('ERROR: unknown request passed to views.invaders')


def inv_distractors(level, onScreen, id):
    letters = sorted(Alphabet.objects.all(), key=lambda x: random.random())
    correct = sorted(invadersUserCorrect.objects.filter(sesh_id=id), key=lambda x: random.random())
    tr = True
    while tr:
        correct = random.choice(letters)
        if correct.letter not in onScreen:
            tr = False
    del letters
    dists = set()
    lettr = correct.letter
    dists.add(lettr)
    sound = correct.sound
    if level == "easy":
        num = 3
        distractors = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=7), key=lambda x: random.random())

        for i in range(len(distractors)):
            if distractors[i].distractor not in onScreen:
                dists.add(distractors[i].distractor)
            if len(dists) == num:
                break


    elif level == "medium":
        num = 4
        distset = set()
        distractors3 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=3), key=lambda x: random.random())
        distractors4 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=4), key=lambda x: random.random())
        distractors5 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=5), key=lambda x: random.random())
        distractors6 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=6), key=lambda x: random.random())
        distractors8 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=8), key=lambda x: random.random())
        distset.update(distractors3)
        distset.update(distractors4)
        distset.update(distractors5)
        distset.update(distractors6)
        distset.update(distractors8)

        if len(distset) < num:
            distractors7 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=7), key=lambda x: random.random())
            distset.update(distractors7)

        for i in distset:
            if i not in onScreen:
                dists.add(i.distractor)
            if len(dists) >= num:
                break

        if len(dists) < num:
            distractors7 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=7), key=lambda x: random.random())
            for i in range(len(distractors7)):
                if distractors7[i] not in onScreen and distractors7[i] not in dists:
                    dists.add(distractors7[i].distractor)
                if len(dists) >= num:
                    break

    elif level == "hard":
        num = 4
        distset = set()
        distractors1 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=1), key=lambda x: random.random())
        distractors2 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=2), key=lambda x: random.random())
        distractors3 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=3), key=lambda x: random.random())
        distractors4 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=4), key=lambda x: random.random())
        distractors5 = LetterDistractor.objects.filter(letter=lettr).filter(type=5)
        distractors6 = LetterDistractor.objects.filter(letter=lettr).filter(type=6)
        distset.update(distractors1)
        distset.update(distractors2)
        distset.update(distractors3)
        distset.update(distractors4)
        distset.update(distractors5)
        distset.update(distractors6)

        if len(distset) < num:
            distractors7 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=7), key=lambda x: random.random())
            distset.update(distractors7)

        for i in distset:
            if i not in onScreen:
                dists.add(i.distractor)
            if len(dists) >= num:
                break

        if len(dists) < num:
            distractors7 = sorted(LetterDistractor.objects.filter(letter=lettr).filter(type=7), key=lambda x: random.random())
            for i in range(len(distractors7)):
                if distractors7[i] not in onScreen and distractors7[i] not in dists:
                    dists.add(distractors7[i].distractor)
                if len(dists) >= num:
                    break


    context = {'letters': list(dists), 'sound':sound, 'game':'double', 'correct':lettr}

    return context



###################################################################


def lemmagame(request, type):
    """
    types: (based on lemma game whiteboard image)
    reception
        wordform in Cree
        wordform audio
            --------
        4 images of distractors
    prod_s (production speaking)
        image of lemma
            --------
        1 audio distractor
        animacy of lemma
    prod_w (production writing)
        image of lemma
            ------
        wordform
    """
def get_lemmagame():
    """
    returns a random lemmagame object
    """
    return sorted(LemmaGame.objects.all().order_by('wordform'), key=lambda x: random.random())[0]

def get_word(game):
    """
    returns the characters of the target word
    """
    return game.wordform.word

def get_audio(game):
    """
    returns the audio filename for the target word

    """
    #get target audio
    target_audio = game.wordform.sound
    #if there is more than one audio
    if "," in target_audio:
        target_audio_as_list = target_audio.split(',')
        print(target_audio_as_list)
        return sorted(target_audio_as_list, key=lambda x: random.random())[0]
    #if there is only one audio file
    else:
        print(target_audio)
        return target_audio

def get_distractors(game, how_many):
    """
    returns a list of Word objects with length (how_many) and the target
    Word object in a random order
    """
    #add the target_word
    return_list = [game.wordform]
    distractors = sorted(game.distractors.all(), key=lambda x:random.random())

    for i in range(how_many):
        return_list.append(distractors[i])
    #randomize the list of distractors
    return sorted(return_list, key=lambda x:random.random())

def get_distractor_images(game, distractors):
    """
    return a list of image filenames based on the list of distractors passed.

    The list should already contain the target word and should already be in
    a randomized order.
    """
    distractor_images = []
    #cycle list of Words, add the image for each Word
    for word in distractors:
        distractor_images.append(word.lemmaID.image)
    return distractor_images

def get_word_image(game):
    return game.lemma.image

    if type == "reception":
        game = get_lemmagame()

        context = {}

        context['word'] = get_word(game)
        context['word_audio'] = get_audio(game)

        #get 4 Word objects as distractors
        distractors = get_distractors(game, 3)
        #pass characters of Word objects to context
        context['distractors'] = [e.word for e in distractors]
        #get filenames of images for Word objects
        context['distractor_images'] = get_distractor_images(game, distractors)
        context['range'] = range(len(distractors))


        if request.method == 'GET':
            return render(request, 'lettergame/lemmagame_reception.html', context)

        elif request.method == 'POST':
            return JsonResponse(context)

        else:
            return HttpResponse('ERROR: request.method was neither GET nor POST')

    if request.method == 'GET':
        return render(request, 'lettergame/lemmagame.html', context)

    elif request.method == 'POST':
        return JsonResponse(context)

    else:
        return HttpResponse('ERROR: request.method was neither GET nor POST')
