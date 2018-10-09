from django.urls import path

from . import views

app_name = 'login'
urlpatterns = [
    path('login/', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.create, name='create')
]
