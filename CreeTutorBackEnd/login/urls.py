from django.urls import path
from django.conf.urls import url

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
    url(r'^activate_user_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_user_account, name='activate_user_account'),
    path('confirm_email/', views.confirm_email, name='confirm_email'),

]
