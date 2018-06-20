from django.urls import path
from . import views

app_name = 'lettergame'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:game>/', views.whichgame, name="whichgame")
]
