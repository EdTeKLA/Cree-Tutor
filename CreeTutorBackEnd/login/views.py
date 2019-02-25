from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

import re

# If user is authenticated, redirect to homepage at lettergame/
# If user is not authenticated, continue to login page
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('lettergame:index'))
    else:
        return render(request, 'login/index.html')

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

            # de-activate user account until email confirmation
            user.is_active = False
            user.save()

            # prepare confirmation email
            current_site = get_current_site(request)
            mail_subject = "Activate your CreeTutor Account"
            message = render_to_string('login/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })

            emailMessage = EmailMessage(mail_subject, message, to=[email])
            emailMessage.send()

            # redirect to email confirmation page
            context = {'redirect': '/confirm_email'}
            return JsonResponse(context)

        else:
            context={'email':email, 'password':password, 'error':error}
            # return(render(request, 'login/index.html', context))
            return JsonResponse(context)

    except KeyError:
        return HttpResponse('ERROR: POST-ed values not received properly')

def profile(request):
    return render(request, "login/profile.html");

def intake(request):
    return render(request, "login/intake.html");

def submit_intake(request):
    # for now just redirect, eventually we need to do something with their answers
    context = {'redirect': '/lettergame'}
    return JsonResponse(context)

def activate_user_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "login/acc_active_complete.html")
    else:
        return HttpResponse('Activation link is invalid!')

def confirm_email(request):
    return render(request, "login/confirm_email.html")
