from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

app_name = 'vocab_lessons'

urlpatterns = [
   path('lesson-<str:level>/', views.ViewSet.as_view(), name="lesson"), # url path to sets
   path('', views.VocabLevel.as_view(), name="index") 
]

urlpatterns += [url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)