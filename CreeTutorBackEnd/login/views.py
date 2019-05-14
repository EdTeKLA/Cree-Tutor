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

from django.urls import reverse
from django.views import View


class Login(View):
    """
    Class was created to show the page where the user can sign up/log in
    """

    def get(self, request):
        """
        Checks if the use is authenticated, if yes, redirects to the home page, otherwise it renders and returns the
        auth page.
        """
        # If the user is authenticated, send them to the homepage
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('lettergame:index'))
        else:
            # Otherwise render a login/signup page
            return render(request, 'login/index.html')

class SignUp(View):
    """
    Class was created to handle the creation of new user accounts.

    It contains methods to verify the infomration submitted is correct as well.
    """

    def post(self, request):
        """
        Method was created to allow a user to create a new account after a few checks have been done.
        """
        try:
            # Getting the sign up information
            email = request.POST['email']
            password = request.POST['password']

            # Check if the email has been used before
            email_valid_error = SignUp.__check_if_email_valid(email)
            if email_valid_error is None:
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
                context={'email':email, 'password':password, 'error':email_valid_error}
                return JsonResponse(context)

        except KeyError as ex:
            print(ex)
            return HttpResponse('ERROR: An unknown error occured.')


    @staticmethod
    def __check_if_email_valid(email):
        """
        Checks if the passed in email is valid(an actual email) and not already in the database.
        - email - The email that will be checked to see if it will be valid
        """
        # Check if the email is valid
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return"Email is invalid"
        elif SignUp.__check_account_exists_with_email(email):
            return "Account already exists"
        else:
            return None

    @staticmethod
    def __check_account_exists_with_email(email):
        """
        Method checks if a user account already exists with this email.
        - email - The email what will be checked to see if it already exists in the database
        """
        # If there is an error, then we know that an account with this email does not exist,
        # so we return False, if the error does not occur, an account does exist and we return True
        try:
            u = User.objects.get(username=email)
            return True
        except User.DoesNotExist:
            return False

class SignIn(View):
    """
    Class was created to sign a user in. Only contains the post method.
    """
    # TODO: FIX THIS SO THAT WHEN YOU HAVEN'T CONFIMED, IT TELLS YOU TO DO SO
    def post(self, request):
        """
        Method that allows a user to log/sign in
        """
        try:
            # Get the auth items
            email = request.POST['email']
            password = request.POST['password']

            # authenticate the user
            user = authenticate(username=email, password=password)

            # If user found, redirect to the homepage
            if user is not None:
                login(request, user)
                context = {'redirect': '/lettergame'}
                return JsonResponse(context)
            else:
                # Try to get the user obejct using the email
                try:
                    user = User.objects.get(username=email)
                except User.DoesNotExist:
                    # Didn't get it, account doesn't exist
                    context = {'error':"No account with this email exists.", 'email':email, 'password':password}
                else:
                    # User found, but the email has not been confirmed, so return an error
                    if not user.is_active:
                        context={'error':"Confirm email to log in.", 'email':email, 'password':password}
                    else:
                        # Some other error occured, most likely the password is wrong.
                        context={'error':"Email or password is incorrect.", 'email':email, 'password':password}
                # Otherwise just return an error saying the login was unsuccessful
                return JsonResponse(context)
        except KeyError as ex:
            print(ex)
            return HttpResponse('ERROR: ' + str(KeyError))

class ActivateAccount(View):
    """
    Class was created to activate a user account using the link sent in the
    email.
    """
    def get(self, request, uidb64, token):
        """
        Activates the account and shows the user their account has been
        activated.
        """
        try:
            # Try to fetch the user
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            # If we found the user, we check the email token to make sure it is
            # valid
            if account_activation_token.check_token(user, token):
                # The token is valid
                # Set is_active to true and return a success page
                user.is_active = True
                user.save()
                return render(request, "login/acc_active_complete.html")
            else:
                # The token is not valid
                return render(request, "login/acc_email_not_valid.html")
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            # If the user can't be fetched we got a problem
            # We tell the user that the activation link is invalid
            return render(request, "login/acc_user_not_found.html")


class SignOut(View):
    """
    Class was created to sign a user out of their account.
    """
    def get(self, request):
        """
        Used to sign a user out
        """
        logout(request)
        return redirect('/')

class Profile(View):
    """
    Class was created to the profile of a user.
    """
    def get(self, request):
        """
        Renders the profile of a user and returns the results.
        """
        return render(request, "login/profile.html")

class SubmitIntake(View):
    """
    Class was created to submit data. For now it does nothing but redirect.
    """
    def get(self, request):
        """
        Just redirects the user. When actaully saving data, use post NOT get.
        """
        context = {'redirect': '/lettergame'}
        return JsonResponse(context)

def intake(request):
    """
    No idea what this does, so I left it as is.
    """
    return render(request, "login/intake.html");

def confirm_email(request):
    """
    Function was created to create an email for a new user account.
    This is left as a function for now
    """
    return render(request, "login/confirm_email.html")
