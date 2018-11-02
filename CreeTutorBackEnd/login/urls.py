from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'login'
urlpatterns = [
    path('login/', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.create, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('intake/', views.intake, name='intake'),
    path('submit_intake/', views.submit_intake, name="submit_intake"), 

    # builtin django password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
