from django.urls import path
from . import views

app_name = 'lettergame'

urlpatterns = [
    path('', views.index, name='index'),
    path('syl/', views.syl_in_word, name="syl"),
    path('<str:game>/', views.whichgame, name="whichgame")
]
