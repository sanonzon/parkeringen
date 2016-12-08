# password email reset base: 
#   http://code.runnable.com/UqMu5Wsrl3YsAAfX/using-django-s-built-in-views-for-password-reset-for-python


from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import User_data
from account.forms import UserDataForm, LoginForm, PasswordResetRequestForm, RegisterForm
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

### Error messages ###

# list of error messages, empty if no errors
# always add ErrorMessages.clear() on initial use
# to avoid old errors being displayed
ErrorMessages = list()

# incorrect login details
IncorrectDetails = "IncorrectDetails"

# user exists
UserExists = "UserExists"

# user exists
PasswordMismatch = "PasswordMismatch"

# invalid registerForm
InvalidForm = "InvalidForm"

# unexpected error
Unexpected = "Unexpected"

### Error messages ###

# Render account login/registration page on request
def Index_screen(request):
    return render(request, Index)

# Render login screen
def Login_screen(request):
    ErrorMessages.clear()

    context = {'LogForm': LoginForm, 'ErrorMessages': ErrorMessages }
    return render(request, Login, context)

# Render register screen
def Register_screen(request):
    ErrorMessages.clear()

    context = {'DataForm': UserDataForm,'RegForm': RegisterForm, 'ErrorMessages': ErrorMessages }
    return render(request, Register, context)

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
    ErrorMessages.clear()

    RegForm = RegisterForm(request.POST or None)
    DataForm = UserDataForm(request.POST or None)
    context = {'DataForm': UserDataForm,'RegForm': RegisterForm, 'ErrorMessages': ErrorMessages }

    ### Validation ###

    # check if username already exists
    Username = RegForm.data['username']
    if not User.objects.filter(username=Username).exists() and Username != "":
        pass
    else:
        # error messages to display
        ErrorMessages.append(UserExists)
        return render(request, Register, context)

    Password = RegForm.data['password']
    Repeat_password = request.POST.get('Repeat_password', '')
    if Password == Repeat_password and Password != "":
            pass
    else:
        # error messages to display
        ErrorMessages.append(PasswordMismatch)
        return render(request, Register, context)

    ### End Validation ###

    if request.POST and RegForm.is_valid() and DataForm.is_valid():
        Password = RegForm.cleaned_data['password']
        Email = RegForm.cleaned_data['email']
        First_name = RegForm.cleaned_data['first_name']
        Last_name = RegForm.cleaned_data['last_name']
        Phone_number = DataForm.cleaned_data['phone_number']
        Repeat_password = request.POST.get('Repeat_password', '')

        if request.user.is_authenticated():
            return redirect('/test') # TODO: redirect to post-login page
        else:
            user = User(username=Username)
            User_Data = User_data(user=user)
            user.email = Email
            user.first_name = First_name
            user.last_name = Last_name
            user.set_password(Password)
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
                # error messages to display
                ErrorMessages.append(Unexpected)
                return render(request, Register, context)

    # error messages to display
    ErrorMessages.append(InvalidForm)
    return render(request, Register, context)

# Log in for registered users
def Login_check(request):
    ErrorMessages.clear()

    LogForm = LoginForm(request.POST)
    context = { 'LogForm': LoginForm, 'ErrorMessages': ErrorMessages }

    if request.POST and LogForm.is_valid():
        Username = LogForm.cleaned_data['username']
        Password = LogForm.cleaned_data['password']

        user = auth.authenticate(username = Username, password = Password)
        if user:
            auth.login(request, user)
            return redirect('/test') # TODO: redirect to post-login page
        else:
            # error messages to display
            ErrorMessages.append(Unexpected)
            return render(request, Login, context)

    # error messages to display
    ErrorMessages.append(IncorrectDetails)
    return render(request, Login, context)
    

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