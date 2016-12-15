# password email reset base: 
# http://code.runnable.com/UqMu5Wsrl3YsAAfX/using-django-s-built-in-views-for-password-reset-for-python

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import User_data, Apartment_number
from account.forms import UserDataForm, LoginForm, PasswordResetRequestForm, RegisterForm, ChangePassword, ChangeDetails
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse

# File locations set as variables due to frequent usage
index = 'account/Index_screen.html'
login = 'account/Login_screen.html'
register = 'account/Register_screen.html'
account_management = 'account/Account_screen.html'
updatePass = 'account/Update_password.html'
updateDetails = 'account/Update_details.html'
forgot_password = 'account/Password_reset_screen.html'

# currently not used
password_confirm = 'account/Password_reset_confirm.html'
# error
authentication_error = 'account/error/Not_authorized.html'
# development only
devtest = 'dev/test.html'

### error messages ###

# list of error messages, empty if no errors
# always add errorMessages.clear() on initial use
# to avoid old errors being displayed
errorMessages = list()

# incorrect login details
incorrectDetails = "IncorrectDetails"
# incorrect password
incorrectPassword = "IncorrectPassword"
# user exists
userExists = "UserExists"
# password exists
passwordMismatch = "PasswordMismatch"
# invalid registerForm
invalidForm = "InvalidForm"
# invalid apartment number
invalidNumber = "InvalidNumber"
# apartment number already in use
numberInUse = "NumberInUse"
# digits only
digitOnly = "IsDigit"
# short username
phoneLength = "PhoneLength"
# short username
usernameLength = "UsernameLength"
# short password
passwordLength = "PasswordLength"
# unexpected error
unexpected = "Unexpected"

### End error messages ###

# class for handling index page functionality
class Index:
    # Render account login/registration page on request
    def Index_screen(request):
        return render(request, index)


# class for handling error functionality
class Error:
    # render authentication error page
    def Authorization_failed(request):
        return render(request, authentication_error)


# class for handling account management functionality
class AccountManagement:
    # render account management page
    @login_required(login_url='/not_authorized')
    def Account_screen(request):
        return render(request, account_management)

    @login_required(login_url='/not_authorized')
    def UpdatePass_screen(request):
        context = {'ChangePass': ChangePassword}
        return render(request, updatePass, context)

    @login_required(login_url='/not_authorized')
    def UpdateDetails_screen(request):
        context = {'ChangeDetails': ChangeDetails}
        return render(request, updateDetails, context)

    @login_required(login_url='/not_authorized')
    def Update_details(request):
        return render(request, account_management)


    # Update user password and update page
    @login_required(login_url='/not_authorized')
    def Update_password(request):
        errorMessages.clear()

        if request.POST:
            ChangePasswordForm = ChangePassword(request.POST)
            context = {'ChangePass': ChangePassword, 'ErrorMessages': errorMessages}

            ### Validation ###

            # true if errors
            error = False

            # raw form data
            current_password = ChangePasswordForm.data['current_password']
            new_password = ChangePasswordForm.data['password']
            repeat_password = ChangePasswordForm.data['repeat_password']

            # check if password do not match
            if new_password != repeat_password:
                error = True
                errorMessages.append(passwordMismatch)

            # check if valid password
            password_valid = request.user.check_password(current_password)
            if not password_valid:
                error = True
                errorMessages.append(incorrectPassword)

            # password minimum length
            if len(new_password) < 4:
                error = True
                errorMessages.append(passwordLength)
            
            # re-render page with all the appended errors
            if error:
                return render(request, updatePass, context)
            else:
                pass

            ### End Validation ###

            if ChangePasswordForm.is_valid():
                current_password = ChangePasswordForm.cleaned_data['current_password']
                new_password = ChangePasswordForm.cleaned_data['password']
                repeat_password = ChangePasswordForm.cleaned_data['repeat_password']

                request.user.set_password(new_password)
                request.user.save()
                logout(request)
                return redirect('/login')          

            # unexpected
            errorMessages.append(unexpected)
            return render(request, updatePass, context)

        else:
            ChangePasswordForm = ChangePassword()
            context = {'ChangePass': ChangePassword, 'ErrorMessages': errorMessages}
            return render(request, updatePass, context)

    # Update user password and update page
    @login_required(login_url='/not_authorized')
    def Update_details(request):

        context = {'ChangeDetails': ChangeDetails}

        if request.POST:
            ChangeDetailsForm = ChangeDetails(request.POST)
            if ChangeDetailsForm.is_valid():
                first_name = ChangeDetailsForm.cleaned_data['first_name']
                last_name = ChangeDetailsForm.cleaned_data['last_name']
                email = ChangeDetailsForm.cleaned_data['email']
                phone_number = ChangeDetailsForm.cleaned_data['phone_number']
                user = User.objects.get(username=request.user.username)
                user_data = User_data.objects.get(user=user)

                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                if email:
                    user.email = email
                user.save()

                if phone_number:
                    user_data.phone_number = phone_number
                user_data.save()

                return redirect('/update_details')
            else:
                return redirect('/update_details')
        else:
            return render(request, updateDetails, context)


# class for handling register functionality
class Register:
    # Render register screen
    def Register_screen(request):
        errorMessages.clear()

        context = {'DataForm': UserDataForm,'RegForm': RegisterForm, 'ErrorMessages': errorMessages }
        return render(request, register, context)

    # Create new user
    def Register_account(request):
        errorMessages.clear()

        RegForm = RegisterForm(request.POST or None)
        DataForm = UserDataForm(request.POST or None)
        context = {'DataForm': UserDataForm,'RegForm': RegisterForm, 'ErrorMessages': errorMessages }

        ### Validation ###

        # true if errors
        error = False

        # form raw data for validation
        username = RegForm.data['username']
        password = RegForm.data['password']
        apartment_number = DataForm.data['apartment']
        phone_number = DataForm.data['phone_number']
        repeat_password = request.POST.get('Repeat_password', '')

        # check if username already exists and is not empty
        if User.objects.filter(username=username).exists():
            error = True
            errorMessages.append(userExists)

        # username minimum length
        if len(username) < 3:
            error = True
            errorMessages.append(usernameLength)

        # password minimum length
        if len(password) < 4:
            error = True
            errorMessages.append(passwordLength)

        # check if provided passwords match
        if password != repeat_password:
            error = True
            errorMessages.append(passwordMismatch)

        # check that the number is not currently in use
        if User_data.objects.filter(apartment=apartment_number).exists():
            error = True
            errorMessages.append(numberInUse)

        # check that the provided apartment exist in Apartment_number
        if not Apartment_number.objects.filter(apartment_number=apartment_number).exists():
            error = True
            errorMessages.append(invalidNumber)

        # if phone number is numbers only
        if phone_number.isdigit():
            error = True
            errorMessages.append(digitOnly)

        # phone number length
        if len(phone_number).strip('\n') < 6:
            error = True
            errorMessages.append(phoneLength)

        # re-render page with all the appended errors
        if error:
            return render(request, register, context)
        else:
            pass

        ### End Validation ###

        if request.POST and RegForm.is_valid() and DataForm.is_valid():
            password = RegForm.cleaned_data['password']
            email = RegForm.cleaned_data['email']
            first_name = RegForm.cleaned_data['first_name']
            last_name = RegForm.cleaned_data['last_name']
            phone_number = DataForm.cleaned_data['phone_number']
            apartment = DataForm.cleaned_data['apartment']
            repeat_password = request.POST.get('Repeat_password', '')

            if request.user.is_authenticated():
                return redirect('/test') # TODO: redirect to post-login page
            else:
                user = User(username=username)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.set_password(password)
                user.is_active = True
                user.save()
                User_Data = User_data(user=user)
                User_Data.phone_number = phone_number
                User_Data.apartment = apartment
                User_Data.save()
                user = auth.authenticate(username = username, password = password)
                if user:
                    auth.login(request, user)
                    return redirect('/test') # TODO: redirect to post-login page
                else:
                    errorMessages.append(unexpected)
                    return render(request, register, context)

        # error messages to display
        errorMessages.append(invalidForm)
        return render(request, register, context)


# class for handling login functionality
class Login:
    # Render login screen
    def Login_screen(request):
        errorMessages.clear()

        context = {'LogForm': LoginForm, 'ErrorMessages': errorMessages }
        return render(request, login, context)

    # Log in for registered users
    def Login_check(request):
        errorMessages.clear()

        context = { 'LogForm': LoginForm, 'ErrorMessages': errorMessages }

        if request.method == 'POST':
            LogForm = LoginForm(request.POST)
            if LogForm.is_valid():
                username = LogForm.cleaned_data['username']
                password = LogForm.cleaned_data['password']

                user = auth.authenticate(username = username, password = password)
                if user:
                    auth.login(request, user)
                    return redirect('/test') # TODO: redirect to post-login page
                else:
                    # if incorrect details
                    errorMessages.append(unexpected)
                    return render(request, login, context)
        else:
            LogForm = LoginForm()

        # if invalid form
        errorMessages.append(incorrectDetails)
        return render(request, login, context)
    

# class for handling logout functionality
class Logout:
    #logout
    def Logout(request):
        logout(request)
        return redirect('/')


# class for handling forgot password functionality(email reset)
class ForgotPassword:
    # Render forgot password screen
    # remove if no longer required
    def Forgot_password_screen(request):
        context = {'form': PasswordResetRequestForm}
        return render(request, forgot_password, context)

    # reset password view using django built in functionality
    def Reset(request):
        # Wrap the built-in password reset view and pass it the arguments
        # like the template name, email template name, subject template name
        # and the url to redirect after the password reset is initiated.

        return password_reset(request, template_name='account/Password_reset_screen.html',
            email_template_name='account/Password_reset_email.html',
            subject_template_name='account/Password_reset_subject.txt',
            post_reset_redirect='/login')

    # display reset confirm view using django built in functionality
    # This view handles password reset confirmation links. See urls.py file for the mapping.
    def Reset_confirm(request, uidb64=None, token=None):
        # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
        # and template name, url to redirect after password reset is confirmed.
        return password_reset_confirm(request, template_name='account/Password_reset_confirm.html',
            uidb64=uidb64, token=token, post_reset_redirect='/login')