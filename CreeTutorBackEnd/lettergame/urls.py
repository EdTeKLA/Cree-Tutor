from django.urls import path
from . import views

app_name = 'lettergame'

urlpatterns = [
    path('', views.index, name='index'),
    path('introsound/<str:game>/', views.letterGames, name="letterGames"),
    path('invaderslevel/', views.invaderslevel, name="invaderslevel"),
    path('invaders/<str:level>/', views.invaders, name="invaders"),
    path('lemmagame/', views.lemmagame, name="lemmagame"),
]
