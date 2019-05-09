from django.urls import path
from . import views

app_name = 'lettergame'

urlpatterns = [
    path('', views.index, name='index'),
    path('invaders/', views.invadersgame, name="invadersgame"), # url path to choose level of difficulty for invaders game
    path('invaders/<str:game>/', views.invaders, name="invaderslevel"), # url path to invaders game
    path('invaders/<str:game>/<str:level>', views.invaders, name="invaders"), # url path to invaders game
    path('introsound/<str:game>/', views.whichGame, name="whichGame"), # url path to choose level of difficulty for letter games
    path('introsound/<str:game>/<str:level>', views.letterGames, name="letterGames"), # url path to letter games
    path('lemmagame/<str:type>', views.lemmagame, name="lemmagame"), # url path to lemma game
]
