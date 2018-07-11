from django.urls import path
from . import views

app_name = 'lettergame'

urlpatterns = [
    path('', views.index, name='index'),
    path('invaders/', views.invaders, name="invaders"),
    path('<str:game>/', views.whichgame, name="whichgame")
]
