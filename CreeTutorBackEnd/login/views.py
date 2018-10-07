from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import models

def login(request):
    if request.method == "POST":
        if request.POST.get("submit") == "log_in":
            # your sign in logic goes here
            print("LOG IN")
            return redirect('login:profile')
        elif request.POST.get("submit") == "sign_up":
            # your sign up logic goes here
            print("SIGN UP")
            pass

    return render(request, "login/index.html")


def profile(request):

    return render(request, "login/profile.html")

