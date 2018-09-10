from django.urls import path
from . import views

app_name = 'lettergame'

urlpatterns = [
    path('', views.index, name='index'),
    path('invaders/<str:level>/', views.invaders, name="invaders"), # url path to invaders game
    path('introsound/<str:game>/', views.whichGame, name="whichGame"), # url path to choose level of difficulty for letter games
    path('introsound/<str:game>/<str:level>', views.letterGames, name="letterGames"), # url path to letter games
    path('invaderslevel/', views.invaderslevel, name="invaderslevel"), # url path to choose level of difficulty for invaders game
    path('lemmagame/<str:type>', views.lemmagame, name="lemmagame"), # url path to lemma game
]
