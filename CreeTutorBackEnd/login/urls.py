from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    path('login/', views.Login.as_view(), name='index'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('signout/', views.SignOut.as_view(), name='signout'),

    # Profile section urls
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/language-info/', views.LanguageInfoViewOld.as_view(), name='profile-language'),
    path('profile/language-info/edit/', views.LanguageInfoView.as_view(), name='profile-language-edit'),
    path('profile/language-info/edit/entry/', views.LanguageEntryView.as_view(), name='language-entry'),
    url(r'^profile/language-info/edit/(?P<pk>[0-9]+)/$', views.LanguageUpdateView.as_view(), name='language-update'),
    url(r'^profile/language-info/edit/(?P<pk>[0-9]+)/delete$', views.LanguageDeleteView.as_view(), name='language-delete'),
    url(r'^language-autocomplete/$', views.LanguageAutocomplete.as_view(), name='language-autocomplete'),
    path('profile/delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
    path('profile/delete/confirm', views.ProfileDeleteConfirmView.as_view(), name='profile-delete-confirm'),

    # Sign up urls
    path('signup/', views.SignUp.as_view(), name='signup'),
    url(r'^activate_user_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ActivateAccount.as_view(), name='activate_user_account'),
    path('confirm_email/', views.confirm_email, name='confirm_email'),
    path('intake/', views.IntakeView.as_view(), name="intake"),

    # Builtin django password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('profile/password/change', views.ChangePasswordView.as_view(), name='password-change')
]
