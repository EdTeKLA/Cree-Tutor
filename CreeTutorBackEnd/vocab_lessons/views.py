import re
from django.shortcuts import (
        get_object_or_404,
        HttpResponseRedirect,
        render,
        redirect
    )
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.contrib import messages

from vocab_lessons.forms import LevelForm
from vocab_lessons.models import VocabLessons, Phrase, Affix

# Create your views here.
class VocabLevel(View):
    """
    Takes in request and loads the vocabmain template
    """
    def get(self, request):
        template_name = 'vocab_lessons/vocabmain.html'
        return render(request, template_name)
    
    def post(self, request):
        if 'level' in request.POST:
            level = request.POST['level']
            request.session['level'] = level
        else:
            messages.error(request, f'Level form submission invalid', extra_tags='danger')
        return redirect('vocab_lessons:lesson', level)

class ViewSet(View):
    def get(self, request, level):
        '''
        Gets set of slides from the database.
        Return slide in set
        '''
        # Get all the objects from vocab_lessons with matching level
        all_vocabs = VocabLessons.objects.all().filter(lesson_no=int(level))
        
        # populate a dictionary with the lesson 
        slides = {}
        for vocab in all_vocabs:
            vocab = vocab.pid
            # create the syllabics and sro string using grams
            phrase_sro = ''
            phrase_syl = ''
            for n in range(1,6):
                phrase = eval('vocab.gram_'+str(n))
                if phrase is not None:
                    # add the prefix if exist
                    prefix = eval('vocab.gram_'+str(n)+'_prefix')
                    if prefix is not None:
                        phrase_sro += prefix.sro
                        phrase_syl += prefix.syl
                    phrase_sro += phrase.word
                    phrase_syl += phrase.syllabics
                    # add the suffix if exist
                    suffix = eval('vocab.gram_'+str(n)+'_suffix')
                    if suffix is not None:
                        phrase_sro += suffix.sro
                        phrase_syl += suffix.syl
                    phrase_sro += ','
                    phrase_syl += ','
            # delete that last comma
            if phrase_sro[-1] == ',':
                phrase_sro = phrase_sro[:-1]
                phrase_syl = phrase_syl[:-1]
            phrase_id = re.sub(r',', '', phrase_sro)
            slides[phrase_id] = {
                'sro' : phrase_sro,
                'syllabic': phrase_syl,
                'image': vocab.image,
                'sound': vocab.sound,
                'translation': vocab.translation,
            }
        return render(request, 'vocab_lessons/viewLesson.html', context={'vocab_slides':slides})
    
    def separate(self, sro, syllabic):
        '''
        Preprocess the sro and syllabic to seperate each morpheme using a comma
        Returns: 
            sro (string)
            syllabic (string)
        '''
        pass