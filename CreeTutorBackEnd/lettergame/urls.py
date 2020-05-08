from django.urls import path
from .views import views, burger_views, verb_conj_views

app_name = 'lettergame'

urlpatterns = [
    path('invaders/<str:level>/', views.Invaders.as_view(), name="invaders"), # url path to invaders game
    path('introsound/<str:game>/', views.WhichGame.as_view(), name="whichGame"), # url path to choose level of difficulty for letter games
    path('introsound/<str:game>/<str:level>', views.LetterGames.as_view(), name="letterGames"), # url path to letter games
    path('invaderslevel/', views.InvadersLevel.as_view(), name="invaderslevel"), # url path to choose level of difficulty for invaders game
    path('burgergame/', burger_views.BurgerGame.as_view(), name="burgerGame"),
    path('burgergame/level_select/', burger_views.BurgerLevelSelect.as_view(), name="burgerGameSelect"),
    path('verb_conjugator/', verb_conj_views.VerbConjGame.as_view(), name="verb_conjugator"),
    path('verb_conjugator/level_select/', verb_conj_views.VerbConjLevelSelect.as_view(), name="verb_conjugator_select")
]
