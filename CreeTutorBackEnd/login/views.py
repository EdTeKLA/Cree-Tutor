from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import logout
from django import forms

import json
import re

# from core.models import Profile
from .tokens import account_activation_token
from login.models import (ModifiedUser, AgeLevels, LanguagesSpoken, UserLanguages, LanguageLevels, Gender)
from .forms import (NameUpdateForm, GenderUpdateForm, AgeRangeUpdateForm, UserLanguageUpdateForm, EmailUpdateForm,
                    ChangePasswordForm)

from dal import autocomplete


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
            return HttpResponseRedirect(reverse('home:index'))
        else:
            # Otherwise render a login/signup page
            return render(request, 'login/index.html')


class SignUp(View):
    """
    Class was created to handle the creation of new user accounts.

    It contains methods to verify the information submitted is correct as well.
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
                SignUp.__purge_inactive_account(email)

                # Create User object
                user = ModifiedUser.objects.create_user(email=email, username=email, password=password)

                # de-activate user account until email confirmation
                user.is_active = False
                user.save()

                # prepare confirmation email
                current_site = get_current_site(request)
                mail_subject = "Activate your CreeTutor Account"
                message = render_to_string('login/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                emailMessage = EmailMessage(mail_subject, message, to=[email])
                emailMessage.send()
                # redirect to email confirmation page
                context = {'redirect': '/confirm_email'}
                return JsonResponse(context)
            else:
                context = {'email': email, 'password': password,
                           'error': email_valid_error}
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
            return "Email is invalid"
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
            u = ModifiedUser.objects.get(username=email, is_active=True)
            return True
        except ModifiedUser.DoesNotExist:
            return False

    @staticmethod
    def __purge_inactive_account(email):
        try:
            u = ModifiedUser.objects.get(username=email)
            u.delete()
            return None
        except ModifiedUser.DoesNotExist:
            return None


class SignIn(View):
    """
    Class was created to sign a user in. Only contains the post method.
    """

    def post(self, request):
        """
        Method that allows a user to log/sign in
        """
        email = request.POST['email']
        password = request.POST['password']

        # authenticate the user
        user = authenticate(username=email, password=password)

        # Do login credentials validate
        if user:
            # Is user authenticated
            if user.is_active:
                login(request, user)
                if user.intake_finished:
                    context = {'redirect': '/'}
                else:
                    context = {'redirect': '/intake/'}
                return JsonResponse(context, status=200)

        context = {'error': "Email or Password is incorrect",
                   'email': email, 'password': password}
        return JsonResponse(context, status=401)


class ActivateAccount(View):
    """
    Class was created to activate a user account using the link sent in the email.
    """

    def get(self, request, uidb64, token):
        """
        Activates the account and shows the user their account has been
        activated.
        """
        try:
            # Try to fetch the user
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = ModifiedUser.objects.get(pk=uid)
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
        except(TypeError, ValueError, OverflowError, ModifiedUser.DoesNotExist):
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


class IntakeView(View):
    """
    Class was created to show the intake form if the user had not completed intake. If the user has completed intake,
    it shows a page which indicates that.

    Also contains a post method which accepts and saves all the information from a completed intake form.
    """

    def get(self, request):
        """
        Shows the intake form if intake has not been completed for the user. If it has been completed, shows a completed
        intake page.
        """
        # Get all the languages
        if self.request.user.intake_finished:
            return render(request, "login/modifieduser_intakesuccess.html")
        else:
            return render(request, "login/modifieduser_intake.html")

    def post(self, request):
        """
        Method was created to update the user record with the first name, last name, age and gender.

        Also creates records for any languages a user knows.
        :param request:
        :return:
        """
        try:
            # Get the user
            user = self.request.user

            # Update the first and the last name
            user.first_name = request.POST['first-name']
            user.last_name = request.POST['last-name']

            # Update the age range
            user.age_range, _ = AgeLevels.objects.get_or_create(
                age_range=request.POST['age-range'])

            # Set the gender
            user.gender, _ = Gender.objects.get_or_create(
                gender=request.POST['gender'])

            # Get all the primary languages
            primary_languages = json.loads(
                request.POST.getlist('primary-language')[0])
            # Save the level of the language

            ll, _ = LanguageLevels.objects.get_or_create(
                language_level='primary')
            print(ll)

            # Save them to the database if they don't exist
            primary_languages_objs = []

            for primary_language in primary_languages:
                ls = {'language': primary_language.lower()}
                ls, _ = LanguagesSpoken.objects.get_or_create(
                    language=primary_language.lower(), defaults=ls)

                ul = UserLanguages(language_spoken=ls,
                                   language_level=ll, user=user)
                ul.save()

            # Dealing with non-primary-languages
            non_primary_languages = json.loads(
                request.POST.getlist('non-primary-languages')[0])
            # Save them to the database if they don't exist
            non_primary_languages_objs = []
            for non_primary_language in non_primary_languages:
                ls = {'language': non_primary_language['language'].lower()}
                ls, _ = LanguagesSpoken.objects.get_or_create(language=non_primary_language['language'].lower(),
                                                              defaults=ls)
                non_primary_languages_objs.append(ls)

                ll, _ = LanguageLevels.objects.get_or_create(
                    language_level=non_primary_language['fluency'].lower())

                ul = UserLanguages(language_spoken=ls,
                                   language_level=ll, user=user)
                ul.save()

            # Saving the status of the intake
            user.intake_finished = True
            # Save the profile
            user.save()
        except Exception as ex:
            print(ex)
            return HttpResponse('ERROR: ' + str(ex))
        else:
            return JsonResponse({'redirect': '/intake'})


class ProfileView(View):
    """
    Class to display the profile of a user and offer ways to change its content
    """

    def get(self, request):
        '''
        Post profile for user
        '''
        # set up the forms
        name_form = NameUpdateForm(user=request.user)
        gender_form = GenderUpdateForm()
        age_form = AgeRangeUpdateForm()
        email_form = EmailUpdateForm()

        # Set up keywords used to refer to the forms by
        context = {
            'user': request.user,
            'name_form': name_form,
            'gender_form': gender_form,
            'age_form': age_form,
            'email_form': email_form
        }
        return render(request, 'login/profile.html', context=context)

    def post(self, request):
        """
        Make changes when the user wants to change something in their profile
        """
        try:
            # Set up the possible forms and assigns the request's user id
            name_form = NameUpdateForm(self.request.POST, instance=self.request.user)
            gender_form = GenderUpdateForm(self.request.POST, instance=self.request.user)
            age_form = AgeRangeUpdateForm(self.request.POST, instance=self.request.user)
            email_form = EmailUpdateForm(self.request.POST, instance=self.request.user)
            # Depending on which form was submited (aka POST-ed) it will update the appropriate
            # value in the database
            if email_form.is_valid():
                # Since we are using emails as username, we need to manually set the username 
                # equal to the newly changed email
                request.user.username = request.user.email
                # Save the form
                email_form.save()
                # Pass a django message to the newly refreshed html to display a sucess message
                messages.success(request, f'Your email was successfully updated!', extra_tags='success')
            elif gender_form.is_valid():
                gender_form.save()
                messages.success(request, f'Your gender information was successfully updated!', extra_tags='success')
            elif age_form.is_valid():
                age_form.save()
                messages.success(request, f'Your age range was successfully updated!', extra_tags='success')
            elif name_form.is_valid():
                name_form.save()
                messages.success(request, f'Your name was successfully updated!', extra_tags='success')
            return redirect('/profile')
        except Exception as ex:
            return HttpResponse('ERROR: ' + str(ex))
        else:
            return JsonResponse({'redirect': '/'})


class LanguageInfoViewOld(View):
    """
    Class to display the language tab of a user and offer ways to edit the languages they know
    """
    model = UserLanguages
    fields = ['language_spoken', 'language_level']

    def get(self, request):
        '''
        Display the general layout of the page
        '''
        # Grab the user language data from database specific to this user
        user_languages = UserLanguages.objects.filter(user=request.user).order_by('language_level')
        # Set up the form names used to refer forms on in the template
        context={'user_languages': user_languages,}
        return render(request, 'login/profile_language.html', context=context)

class LanguageAutocomplete(autocomplete.Select2QuerySetView):
    '''
    Class which returns a query set of all the languages stored in the language_spoken table
    '''
    def get_queryset(self):
        languages_query = LanguagesSpoken.objects.all()
        if self.q:
            languages_query = languages_query.filter(language__startswith=self.q)
        return languages_query

class LanguageInfoView(ListView):
    model = UserLanguages
    # set the tempelate
    template_name = 'login/profile_language_edit.html'
    # set up the name the user languages will be refered as
    context_object_name = 'user_languages'
    # Order the posts by the 
    ordering = ['language_level']
    def get_queryset(self):
        # Filter through all the languages in the user_language table to get a query of only
        # the languages spoken by this user and order it by language level (primary-1 and so on)
        user_languages = UserLanguages.objects.filter(user=self.request.user).order_by('language_level')
        return user_languages

class LanguageEntryView(CreateView):
    model = UserLanguages
    template_name = 'login/profile_language_form.html'
    # Set up the form class so that django know
    form_class = UserLanguageUpdateForm 
    # Link to the main language edit page after successfully adding a language to this user
    success_url = reverse_lazy('login:profile-language-edit')
    def form_valid(self, form):
        '''Set up the form validation so that the user column in the userlanguage table is not empty'''
        # Set the language entry's user to the user sending the POST request
        form.instance.user = self.request.user
        # Raise a success message to display on the reloaded html page
        messages.success(self.request, f'Your language was successfully added!', extra_tags='success')
        # apply the changes and save
        return super().form_valid(form)
    
class LanguageUpdateView(UpdateView):
    model = UserLanguages
    template_name = 'login/profile_language_form.html'
    form_class = UserLanguageUpdateForm 
    success_url = reverse_lazy('login:profile-language-edit')
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'Your language was successfully updated!', extra_tags='success')
        return super().form_valid(form)

class LanguageDeleteView(DeleteView):
    model = UserLanguages
    success_url = reverse_lazy('login:profile-language-edit')
    def delete(self, request, *args, **kwargs):
        # Set up a success message for when user's language is successfully deleted
        messages.success(self.request, f'Your languages was successfully deleted', extra_tags='success')
        return super(LanguageDeleteView, self).delete(request, *args, **kwargs)

class ChangePasswordView(View):
    def get(self, request):
        """
        Render the original password change page
        """
        password_form = ChangePasswordForm(request.user)
        return render(request, 'login/password_change_form.html',context={'password_form':password_form})

    def post(self, request):
        """
        Change the password for users
        """
        try:
            password_form = ChangePasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                # necessary step to stay logged into the account with the password changed
                update_session_auth_hash(request, password_form.user)
                messages.success(request, f'Your password was successfully updated!')
                return redirect('profile')
            else:
                messages.error(request, f'An error has occured, please try again.')
        except Exception as ex:
            return HttpResponse('ERROR: ' + str(ex))
        else:
            return JsonResponse({'redirect': '/'})

class ProfileDeleteView(View):
    def get(self, request):
        '''
        Display profile delete page
        '''
        return render(request, 'login/profile_delete.html')

class ProfileDeleteConfirmView(View):
    def get(self, request):
        '''
        Display profile delete confirmation page
        '''
        return render(request, 'login/profile_delete_confirm.html')
    
    def post(self, request):
        '''
        Execute user profile deletion
        '''
        try:
            # Due to some constraints on the system because of the user dependencies
            # in other apps (e.g. shadowing) we are unable to delete the account fully
            # the Django documents recommends to just set is_active to False which is
            # what is done here.
            # TO DO: Look into the dependencies and allow for the user and the user data
            # to be all deleted together using user.delete()

            # Set the current user as the user who sent out the POST request
            user = ModifiedUser.objects.get(pk=request.user.pk)
            # Set the user's active state as false which disables the account
            user.is_active = False
            # Set the user's email and username to empty so that if this email is used again to 
            # create another account it is allowed
            user.email = None
            user.username = None
            # save everything
            user.save()
            # redirect user to the account deltion completion page
            return HttpResponseRedirect(reverse_lazy('login:profile-delete-complete'))
        except Exception as ex:
            return HttpResponse('ERROR: ' + str(ex))
        else:
            return JsonResponse({'redirect': '/'})

class ProfileDeleteCompleteView(View):
    def get(self, request):
        '''
        Display profile delete complete page
        '''
        return render(request, 'login/profile_delete_complete.html')

# sample user profile update
def confirm_email(request):
    """
    Function was created to create an email for a new user account.
    This is left as a function for now
    """
    return render(request, "login/confirm_email.html")
