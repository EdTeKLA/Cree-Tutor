from django.urls import path

from . import views

app_name = 'errorpages'
urlpatterns = [
    path('view_404/', views.view_404, name='view_404'),
    path('view_500/', views.view_500, name='view_500'),
]