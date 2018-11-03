from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import Http404

"""
Note that in order to view these custom error pages in a local environment
you'll have to set:
- settings.DEBUG = False
- settings.TEMPLATE_DEBUG = False
- settings.ALLOWED_HOSTS = ['*']

Also start the runserver command with the "--insecure" flag to force
the serving of static files locally despite DEBUG = False. (SHOULD ONLY 
SET THIS FLAG FOR DEBUG PURPOSES)
"""
def view_404(request, exception, template_name='errorpages/404.html'):
    """
    Render custom 404 page
    """
    return render(request, template_name)

def view_500(request, template_name='errorpages/500.html'):
    """
    Render custom 500 page
    """
    return render(request, template_name)