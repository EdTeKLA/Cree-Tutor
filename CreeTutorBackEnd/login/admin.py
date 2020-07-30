from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import Group

from .models import ModifiedUser as User
from .models import UserLanguages, LanguagesSpoken
from .forms import UserAdminChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ['first_name',
                                      'last_name',
                                      'age_range',
                                      'gender']}),
        # # A better way of displaying language has to be made
        # ('Language info', {'fields': ('language_spoken',
        #                               'language_level'
        #                               )}),
        ('Permissions', {'fields': ['is_active',
                                    'is_staff',
                                    'is_superuser', ]}),
        ('Intake status', {'fields': ['intake_finished', ]}),
        ('Account activity details', {'fields': ['date_joined',
                                                 'last_login']}),
    ]

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(UserLanguages)
admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)