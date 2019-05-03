from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    path('login/', views.Login.as_view(), name='index'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('signout/', views.SignOut.as_view(), name='signout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('intake/', views.intake, name='intake'),
    path('submit_intake/', views.SubmitIntake.as_view(), name="submit_intake"),
    path('submit_intake/', views.SubmitIntake.as_view(), name="submit_intake"),
    url(r'^activate_user_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ActivateAccount.as_view(), name='activate_user_account'),
    path('confirm_email/', views.confirm_email, name='confirm_email'),

    # builtin django password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
