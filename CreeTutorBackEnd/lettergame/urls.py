from django.urls import path
from . import views

app_name = 'lettergame'

urlpatterns = [
    path('', views.index, name='index'),
    path('invaders/<str:level>/', views.invaders, name="invaders"),
    path('introsound/<str:game>/', views.whichGame, name="whichGame"),
    path('introsound/<str:game>/<str:level>', views.letterGames, name="letterGames"),
    path('invaderslevel/', views.invaderslevel, name="invaderslevel"),
    path('lemmagame/', views.lemmagame, name="lemmagame")
]
