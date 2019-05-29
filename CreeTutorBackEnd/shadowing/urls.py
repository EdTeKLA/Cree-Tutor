from django.urls import path

from . import views

app_name = 'shadowing'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('story/<int:story_index>/', views.Shadowing.as_view(), name='story'),
    path('log/<int:story_id>/<str:action>/<time>/', views.ShadowingLogging.as_view(), name='logging'),
    path('feedback/<int:story_id>/', views.ShadowingFeedBack.as_view(), name='feedback')
]
