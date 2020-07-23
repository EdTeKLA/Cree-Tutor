from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Submit, Row, Column, Field, ButtonHolder, HTML, Div, MultiField, Button)
from crispy_forms.bootstrap import FormActions

from .models import ModifiedUser as User
from .models import UserLanguages, LanguagesSpoken

from dal import autocomplete

class NameUpdateForm(forms.ModelForm):
    '''
    Form that updates the user's first and last name. It contains all components of the form, including the submit and cancel buttons.
    It is formatted using crispy-forms through their Layout class. Read more at: https://django-crispy-forms.readthedocs.io/en/d-0/layouts.html 
    '''
    def __init__(self, *args, **kwargs):
        # Get user information
        self.user = kwargs.pop('user')
        # Call super to inherit instances and needed methods from the parent class
        super(NameUpdateForm, self).__init__(*args, **kwargs)
        # Set up the form helper
        self.helper = FormHelper()
        # Set the class of the form to horizontal for nice inline display
        self.helper.form_class = 'form-horizontal'
        # Set the label to not be displayed
        self.helper.label_class = 'sr-only'
        # Set the classes of each field to all be form-inline
        self.helper.field_class = 'form-inline'
        # Build the form layout using Layout()
        self.helper.layout = Layout(
            Row(
                # TO DO: I can't see to get the value to the name into placeholders
                # so these are hardcoded in just for now until a solution is found
                # if we can get the first name through USER that would be great but it doesnt work 
                # e.g. f'{username}' 
                Column(Field('first_name', placeholder=self.user.first_name, css_class="form-control mx-1 col-10")),
                Column(Field('last_name', placeholder=self.user.last_name, css_class="form-control mx-1 col-10")),
                css_class="form-group mx-3 mb-1 inline"
            ),
            # Enclose all the submit and cancel buttons in a div called FormActions (recommended as per crispy-form documentations)
            FormActions(
                Submit('submit', value='Update', css_class='btn btn-primary btn-sm inline mr-1'),
                Button('cancel', value='Cancel', css_class='text-muted btn-sm inline', css_id="name-form-cancel-button"),
                css_class="mt-1 mb-1 mx-1 inline"
            )
        )
    class Meta:
        # Since this class inherits from ModelForm we need to provide the model that has all can access the right tables in the database
        model = User
        # Set up which fields we want to display using this form
        fields = ['first_name', 'last_name']

class GenderUpdateForm(forms.ModelForm):
    '''
    Form that updates the user's gender. It contains all components of the form, including the submit and cancel buttons.
    It is formatted using crispy-forms through their Layout class. Read more at: https://django-crispy-forms.readthedocs.io/en/d-0/layouts.html 
    '''
    def __init__(self, *args, **kwargs):
        super(GenderUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'form-inline'
        self.helper.layout = Layout(
            Field('gender', css_class="row form-control mb-1 ml-3"),
            FormActions(
                Submit('submit', value='Update', css_class='btn btn-primary btn-sm inline mr-1'),
                Button('cancel', value='Cancel', css_class='text-muted btn-sm inline', css_id="gender-form-cancel-button"),
                # So far all of these have a ml-4 because I could not find a better way to format it so it would work
                # TO DO: look into bootstrap so that this formating is more dynamic
                css_class="row mt-1 mb-1 mx-1 inline"
            )
        )
    class Meta:
        model = User
        fields = ['gender']

class AgeRangeUpdateForm(forms.ModelForm):
    '''
    Form that updates the user's age range. It contains all components of the form, including the submit and cancel buttons.
    It is formatted using crispy-forms through their Layout class. Read more at: https://django-crispy-forms.readthedocs.io/en/d-0/layouts.html 
    '''
    def __init__(self, *args, **kwargs):
        super(AgeRangeUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'form-inline'
        self.helper.layout = Layout(
            Field('age_range', css_class="form-control mb-1 ml-3"),
            FormActions(
                Submit('submit', value='Update', css_class='btn btn-primary btn-sm inline mr-1'),
                Button('cancel', value='Cancel', css_class='text-muted btn-sm inline', css_id="age-form-cancel-button"),
                css_class="mt-1 mb-1 mx-1 inline"
            )
        )
    class Meta:
        model = User
        fields = ['age_range']

class EmailUpdateForm(forms.ModelForm):
    '''
    Form that updates the user's email. It contains all components of the form, including the submit and cancel buttons.
    It is formatted using crispy-forms through their Layout class. Read more at: https://django-crispy-forms.readthedocs.io/en/d-0/layouts.html 
    '''
    # explicitly state that the input in the email field is of EmailField type which automatically checks for a general email format
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super(EmailUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'form-inline'
        self.helper.layout = Layout(
            Field('email', placeholder='Email', css_class="form-control mb-1 ml-3 mr-1"),
            FormActions(
                Submit('submit', value='Update', css_class='btn btn-primary btn-sm inline mr-1'),
                Button('cancel', value='Cancel', css_class='text-muted btn-sm inline', css_id="email-form-cancel-button"),
                css_class="inline ml-5"
            )
        )
    class Meta:
        model = User
        fields = ['email']

class ChangePasswordForm(PasswordChangeForm):
    '''
    Form that updates the user's password while keeping them signed in. It contains all components of the form, 
    including the submit and cancel buttons
    It is formatted using crispy-forms through their Layout class. Read more at: https://django-crispy-forms.readthedocs.io/en/d-0/layouts.html 
    '''
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-5'
        self.helper.field_class = 'col-5'
        self.helper.layout = Layout(
            Div(
                HTML("""<p>To change your password, fill out the following form and submit it. </p>"""),
                Field('old_password', css_class="col-12 form-control"),
                Field('new_password1', css_class="col-12 form-control"),
                Field('new_password2', css_class="col-12 form-control"),
                css_class="col-7 list-group-item box-display mb-3"
                ),
            FormActions(
                Submit('submit', value='Update', css_class='btn btn-primary'),
                # Cannot use Button with type cancel because it cannot link the user to another page like <a> can
                HTML(""" 
                    <a type="button" class="btn btn-light text-muted" id="form-cancel-button" href="{%url 'login:profile'%}">
                        Cancel
                    </a>
                    """),
                css_class="form-group row mx-1"
            ),
        )

class UserLanguageUpdateForm(forms.ModelForm):
    '''
    Form that acts allows users to either update or add a language they speak into their language information section. 
    It contains all components of the form, including the submit and cancel buttons. It is formatted using crispy-forms 
    through their Layout class. Read more at: https://django-crispy-forms.readthedocs.io/en/d-0/layouts.html 
    '''
    def __init__(self, *args, **kwargs):
        super(UserLanguageUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('language_spoken', placeholder='Type a language here...', css_class="form-control col-10 mx-2"),
                Field('language_level', css_class="form-control col-10 mx-2"), 
                css_class='col-12 list-group-item box-display mb-3'
            ),
            FormActions(
                Submit('submit', value='Submit', css_class='btn btn-primary inline mr-1'),
                HTML("""
                    <a type="button" class="btn btn-light text-muted inline" href='{% url "login:profile-language-edit"%}'>Cancel</a>
                """),
                css_class="mx-1"
            )
        )
    class Meta:
        model = UserLanguages
        fields = ['language_spoken','language_level']
        # To set up autocomplete the widget which enables django-autocomplete-light must be set up
        # It needs a path to the autocomplete view
        widgets = {
            'language_spoken' : autocomplete.ModelSelect2(url='login:language-autocomplete'),
        }

class UserAdminChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_staff', 'is_superuser', 'first_name', 'last_name',
                  'username', 'age_range', 'gender', 'intake_finished', 'date_joined', 'last_login')
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]