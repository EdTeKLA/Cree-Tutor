from re import compile
from django.http import HttpResponseRedirect
from django.conf import settings

""" 
list containing URLs (compiled as regex objects)
that users are allowed to access without logging in.
"""
noLoginUrls = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'NO_LOGIN_URL'):
    for url in settings.NO_LOGIN_URL:
        noLoginUrls.append(compile(url))

def requireLogin_middleware(get_response):
    """ 
    Middleware that redirects the user to the login page if not logged in 
    and trying to request a page not under settings.NO_LOGIN_URL
    """
    def middleware(request):
        if not (request.user.is_authenticated):
            path = request.path_info.lstrip('/')
            if not (any(u.match(path) for u in noLoginUrls)):
                return HttpResponseRedirect(settings.LOGIN_URL)
            else:
                response = get_response(request)
                return response
        else:
            response = get_response(request)
            return response
    return middleware
