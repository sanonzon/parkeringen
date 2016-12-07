# password email reset base:
#   http://code.runnable.com/UqMu5Wsrl3YsAAfX/using-django-s-built-in-views-for-password-reset-for-python


from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import User_data
from account.forms import UserDataForm, UserForm, PasswordResetRequestForm, PasswordChangeForm
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse

# File locations set as variables due to frequent usage
Index = 'account/Index_screen.html'
Login = 'account/Login_screen.html'
Register = 'account/Register_screen.html'
Account_management = 'account/Account_screen.html'
Forgot_password = 'account/Password_reset_screen.html'

# currently not used
Password_confirm = 'account/Password_reset_confirm.html'

# error
Authentication_error = 'account/error/Not_authorized.html'

# development only
Devtest = 'dev/test.html'



# Render account login/registration page on request
def Index_screen(request):
    return render(request, Index)

# Render login screen
def Login_screen(request):
    return render(request, Login)

# Render register screen
def Register_screen(request):
    return render(request, Register)

# Render forgot password screen
def Forgot_password_screen(request):
    context = {'form': PasswordResetRequestForm}
    return render(request, Forgot_password, context)

# render account management page
@login_required(login_url='/not_authorized')
def Account_screen(request):
    return render(request, Account_management)

# render authentication error page
def Authorization_failed(request):
    return render(request, Authentication_error)

# Update user password and update page
@login_required(login_url='/not_authorized')
def Update_password(request):
    Current_password = request.POST.get('Current_password', '')
    New_password = request.POST.get('New_password', '')
    Repeat_password = request.POST.get('Repeat_password', '')

    Password_valid = request.user.check_password(Current_password)
    if Password_valid:
        if New_password == Repeat_password:
            request.user.set_password(New_password)
            request.user.save()
            return redirect('/logout')
        else:
            return render(request, Account_management) # TODO: render error
    else:
        return redirect('/') # TODO: render error page

# Create new user
def Register_account(request):
    Username = request.POST.get('Username', '')
    Password = request.POST.get('Password', '')
    Email = request.POST.get('Email_address', '')
    First_name = request.POST.get('First_name', '')
    Last_name = request.POST.get('Last_name', '')
    Phone_number = request.POST.get('Phone_number', '')
    Repeat_password = request.POST.get('Repeat_password', '')

    if request.user.is_authenticated():
        return redirect('/test') # TODO: redirect to post-login page
    else:
        if not User.objects.filter(username=Username).exists() and Username != "":
            user = User(username=Username)
            User_Data = User_data(user=user)
            user.email = Email
            user.first_name = First_name
            user.last_name = Last_name
            if Password == Repeat_password and Password != "":
                user.set_password(Password)
            else:
                return redirect("/") # TODO: render error page
            user.is_active = True
            user.save()
            User_Data = User_data(user=user)
            User_Data.phone_number = Phone_number
            User_Data.save()
            user = auth.authenticate(username = Username, password = Password)
            if user:
                auth.login(request, user)
                return redirect('/test') # TODO: redirect to post-login page
            else:
                return redirect('/') # TODO: render error page
        else:
            return redirect("/") # TODO: render error page

# Log in for registered users
def Login_check(request):
    Username = request.POST.get('Username', '')
    Password = request.POST.get('Password', '')

    user = auth.authenticate(username = Username, password = Password)
    if user:
        auth.login(request, user)
        return redirect('/test') # TODO: redirect to post-login page
    else:
        return redirect('/login') # TODO: render login error page


#logout
def Logout(request):
    logout(request)
    return redirect('/')

# reset password view using django built in functionality
def reset(request):
    # Wrap the built-in password reset view and pass it the arguments
    # like the template name, email template name, subject template name
    # and the url to redirect after the password reset is initiated.
    return password_reset(request, template_name='account/Password_reset_screen.html',
        email_template_name='account/Password_reset_email.html',
        subject_template_name='account/Password_reset_subject.txt',
        post_reset_redirect='/login')

# display reset confirm view using django built in functionality
# This view handles password reset confirmation links. See urls.py file for the mapping.
def reset_confirm(request, uidb64=None, token=None):
    # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
    # and template name, url to redirect after password reset is confirmed.
    return password_reset_confirm(request, template_name='account/Password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect='/login')
