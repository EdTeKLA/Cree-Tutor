from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import models


def uniqueEmail(email):
    try:
        u = User.objects.get(username=email)
    except User.DoesNotExist:
        u = None

    if u != None:
        return False
    else:
        return True

def checkEmail(email):
    error=None
    if not uniqueEmail(email):
        error = "That email is already taken."
    elif '@' not in email:
        error = "That is not a valid email address."
    elif len(email) < 6:
        error = "That is not a long enough email"
    return error

def index(request):

    return render(request, 'login/index.html')

def signin(request):
    try:
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('lettergame:index')
        else:
            context={'error':"Email or password is incorrect.", 'email':email, 'password':password}
            return render(request, 'login/index.html', context)

    except KeyError:
        return HttpResponse('ERROR: ' + str(KeyError))


def signout(request):
    logout(request)
    return redirect('login:index')

def create(request):
    try:
        email = request.POST['email']
        password = request.POST['password']

        error = checkEmail(email)

        if error == None:
            # Create User object
            user = User.objects.create_user(email, email, password)

            # Log user in
            login(request,user)

            user.save()
            return redirect('lettergame:index')

        else:
            context={'email':email, 'password':password, 'error':error}
            return(render(request, 'login/index.html', context))

    except KeyError:
        return render(request, 'login/index.html')
