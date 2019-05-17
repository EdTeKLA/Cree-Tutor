from django.urls import path

from . import views

app_name = 'shadowing'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('story/<int:story_index>/', views.Shadowing.as_view(), name='story'),
]
