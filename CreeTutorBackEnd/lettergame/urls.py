from django.urls import path
from . import views

app_name = 'lettergame'

urlpatterns = [
    path('invaders/<str:level>/', views.Invaders.as_view(), name="invaders"), # url path to invaders game
    path('introsound/<str:game>/', views.WhichGame.as_view(), name="whichGame"), # url path to choose level of difficulty for letter games
    path('introsound/<str:game>/<str:level>', views.LetterGames.as_view(), name="letterGames"), # url path to letter games
    path('invaderslevel/', views.InvadersLevel.as_view(), name="invaderslevel"), # url path to choose level of difficulty for invaders game
]
