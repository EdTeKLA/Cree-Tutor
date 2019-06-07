"""
File contains all the helpers needed by views in views.py
"""

import random
from .models import *


def getOptions(option, type, level):
    """
    Function retrieves options for both single and double letter game. How many options depends on level.
    Currently picks distractors at random.
    Return dictionary "context" containing information on the level, options, correct answer, and sound path.
    """
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
    """
    Function takes in parameters about the post request (request), the models the
    data should be submitted to, and the data that needs submitting
    Submits data and returns nothing
    """

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
    answer.user_id = request.user.id
    answer.level = GameLevels.objects.get(name = level)
    answer.session_id = request.POST['session_id']
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
        answer_dist.session_id = request.POST['session_id']
        answer_dist.save()
    # Insert the distractors
    for i in dists:
        distractors = whichDist()
        distractors.distractor = option.objects.get(pk = i)
        distractors.answer_id = a_id
        distractors.session_id = request.POST['session_id']
        distractors.save()

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
