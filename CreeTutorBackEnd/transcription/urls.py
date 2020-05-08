from django.urls import path

from . import views

app_name = 'transcription'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('story/<int:story_index>/', views.Transcription.as_view(), name='story'),
    path('log/<int:story_id>/<str:action>/<time>/<str:session_id>/<str:transcription>/',
         views.TranscriptionLogging.as_view(), name='logging'),
    path('feedback/<int:story_id>/<str:session_id>/', views.ShadowingFeedBack.as_view(), name='feedback'),
]
