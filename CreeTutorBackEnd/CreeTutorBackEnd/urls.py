"""CreeTutorBackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('vocab_lessons/', include('vocab_lessons.urls', namespace='vocab_lessons')),
    path('', include('login.urls')),
    path('', include('home.urls')),
    path('lettergame/', include('lettergame.urls')),
    path('shadowing/', include('shadowing.urls')),
    path('transcription/', include('transcription.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('errorpages/', include('errorpages.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'errorpages.views.view_404'
handler500 = 'errorpages.views.view_500'
