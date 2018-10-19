from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
import re

def uniqueEmail(email):
    try:
        u = User.objects.get(username=email)
    except User.DoesNotExist:
        u = None

    if u is not None:
        return False
    else:
        return True

def checkEmail(email):
    error = None
    if not uniqueEmail(email):
        error = "Account already exists"
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        error = "Email is invalid"
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
            context = {'redirect': '/lettergame'}
            return JsonResponse(context)
        else:
            context={'error':"Email or password is incorrect.", 'email':email, 'password':password}
            return JsonResponse(context)

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

        if error is None:
            # Create User object
            user = User.objects.create_user(email, email, password)
            user.save()

            # Log user in
            user = authenticate(username=email, password=password)
            login(request, user)

            context = {'redirect': '/profile'}
            return JsonResponse(context)

        else:
            context={'email':email, 'password':password, 'error':error}
            # return(render(request, 'login/index.html', context))
            return JsonResponse(context)


    except KeyError:
        return HttpResponse('ERROR: POST-ed values not received properly')

def profile(request):
    username = request.user.username
    return render(request, "login/profile.html", {'username': username});