from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from account.models import User_data

# Define an inline admin descriptor for user_data model
class UserDataInline(admin.StackedInline):
    model = User_data
    can_delete = False
    verbose_name_plural = 'user data'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserDataInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
