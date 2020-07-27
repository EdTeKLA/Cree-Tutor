"""
File contains all the helpers needed by views in views.py
"""

import random
from random import choice
from ..models import *
import re


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
    answer.level = GameLevels.objects.get(level = level)
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

def reroll(level, verb, vowels):
    reroll = False;
    if (level == "easy" or level == "medium"):
        for j in range(4):
            if verb.word[0] == vowels[j]:
                reroll = True
    return reroll

def recipe_maker(level):
      '''
      model querying here to get the verbs and the conjugation for the Burger Game application
      '''



      vowels = ["a", "e", "i", "o", "u"]

      verb_objects = sorted(Creedictionarydotcom.objects.filter(pos="VAI"), key=lambda x: random.random())  # this is for retrieving all objects with VAI verbs

      if reroll(level, verb_objects[0], vowels) == True:
          verb_objects = sorted(Creedictionarydotcom.objects.filter(pos="VAI"), key=lambda x: random.random())

      verb = verb_objects[0]

      '''
      chops the w off the verb, if there is one
      '''
      for j in range(4):
          if verb_objects[j].word[-1] == "w":
            verb_objects[j].word = verb_objects[j].word[:-1]

      '''
      Returns context for burgergame.
      '''
      '''
      Below searches the verb for special rules that must be applied to in during conjugation. Inde_or_conj is so the correct joiner is used,
      and person is so that the final e to a is used properly. 
      '''
      # TODO: still doesn't work right
      # What doesn't work right? Blocker, need to walk through logic with delaney to figure out what is going on
      # and what needs to be changed.


      inde_or_conj = choice(list(set(["independent", "conjunct"])))
      person = choice(list(set(["1S", "2S", "3S", "2I", "1P", "2P", "3P", "3'"])))
      # TODO: DETERMINE WHAT verb_sperule means
      verb_sperule = "";
      verb_joiner = "";

      if (inde_or_conj == "independent"):
          for i in range(4):
             verb_joiner = "h" if verb.word[0] == (vowels[i]) else ""

      else:
          verb_joiner = "final e to â" if (person == "1S" or person == "2S" or person == "2I" or person == "1P" or person == "2P") and verb.word[-1] == "e" else ""
          for i in range(4):
            verb_joiner = "t" if verb.word[0] == (vowels[i]) else ""

      random_conjugation = sorted(recipe.objects.all(), key=lambda x: random.random())
      conjugation = sorted(recipe.objects.filter(independent_or_conjunct=inde_or_conj).filter(pronoun=person), key=lambda x: random.random())

      regex = re.compile('(S\/he )|(him\/her)|(they all)|you|the tree|s\/he|her\/his|his\/her|they ')


      line = verb.translation  # using some string
      new_line = regex.sub(' ', line)  # take out what we specified in regex, substitute it with something else. This example substitutes it with a space.
      # the value at new_line is now  = 'some string"

      regex = re.compile(' is ')
      new_line = regex.sub('', new_line)
      regex = re.compile(' goes ')
      new_line = regex.sub(" go ", new_line)
      prefix = conjugation[0].prefix
      suffix = conjugation[0].suffix
      translation = conjugation[0].translation
      conjugation_list = [inde_or_conj, person, verb_sperule, verb_joiner, prefix, suffix, translation]
      conjugation_dict = {
          "inde_or_conj": inde_or_conj,
          "person":person,
          "verb_sperule":verb_sperule,
          "joiner":verb_joiner,
          "prefix":prefix,
          "suffix":suffix,
          "translation":translation,
          "verb":verb.word
      }


      new = ""
      if (inde_or_conj == "independent"):
          if (conjugation_list[1] == "1S"):
            new = "my"
          elif (conjugation_list[1] == "2S" or conjugation_list == "2P"):
            new = "your"
          elif (conjugation_list[1] == "3S" or conjugation_list[1] == "3'"):
            new = "his/her"
          elif (conjugation_list[1] == "1P" or conjugation_list == "2I"):
            new = "our"
          elif (conjugation_list[1] == "3P"):
            new = "their"

      new_line = re.sub('his\/her', new, new_line)

      if (inde_or_conj == "conjunct"):
          if (conjugation_list[1] == "1P" or conjugation_list[1] == "2I" or conjugation_list[1] == "2P" or conjugation_list[1] == "3P" or conjugation_list[1] == "2S"):
              new_line = ("ALTare " + new_line)
          elif (conjugation_list[1] == "1S"):
              new_line = ("ALTam " + new_line)
          else:
              new_line = ("is " + new_line)

      # else:
          # if (conjugation_list[1] == "1S" or conjugation_list[1] == "2S" or conjugation_list[1] == "1P" or conjugation_list[1] == "2I" or conjugation_list[1] == "2P" or conjugation_list[1] == "3P"):
          #     regex = re.compile('.+(s)')
          #     new_line = regex.sub('', new_line)


      verbs = [verb.word, new_line]

      prefix_distractors = [conjugation[0].prefix, random_conjugation[0].prefix, random_conjugation[1].prefix, random_conjugation[2].prefix]
      verb_distractors = [verb_objects[0].word, verb_objects[1].word, verb_objects[2].word, verb_objects[3].word]
      suffix_distractors = [conjugation[0].suffix, random_conjugation[0].suffix, random_conjugation[1].suffix, random_conjugation[2].suffix]
      '''
      conjugation_list and verb are the recipe/answer key. they will never be shown on screen. prefix_distractors,
       verb_disctractors, and suffix_distractors WILL be expressed, and will be what shows up on the ingredients.
      '''
      context = {'conjugation_list': conjugation_dict,
                 'verb': verbs,
                 'prefix_distractors': prefix_distractors,
                 'verb_distractors': verb_distractors,
                 'suffix_distractors': suffix_distractors,
                 'level' : level
                 }
      return context

