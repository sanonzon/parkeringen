# password email reset base: 
# http://code.runnable.com/UqMu5Wsrl3YsAAfX/using-django-s-built-in-views-for-password-reset-for-python

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import User_data, Apartment_number
from account.forms import LoginForm, PasswordResetRequestForm, RegisterForm, ChangePassword, ChangeDetails, PasswordChangeForm
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse

# File locations set as variables due to frequent usage
index = 'account/Index_screen.html'
faq = 'account/information/FAQ_screen.html'
login = 'account/Login_screen.html'
register = 'account/Register_screen.html'
account_management = 'account/Account_screen.html'
updatePass = 'account/Update_password.html'
updateDetails = 'account/Update_details.html'
forgot_password = 'account/Password_reset_screen.html'
password_confirm = 'account/Password_reset_confirm.html'

# error
authentication_error = 'account/error/Not_authorized.html'
# development only
devtest = 'dev/test.html'

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
        context = {'ChangePass': ChangePassword(request.user)}
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
        context = {'ChangePass': ChangePassword(request.user)}

        if request.POST:
            change_password_form = ChangePassword(request.user, request.POST)

            if change_password_form.is_valid():
                current_password = change_password_form.cleaned_data['current_password']
                new_password = change_password_form.cleaned_data['password']
                repeat_password = change_password_form.cleaned_data['repeat_password']

                request.user.set_password(new_password)
                request.user.save()

                user = auth.authenticate(username = request.user.username, password = new_password)
                auth.login(request, user)
                
                return redirect('/account_management')
            else:
                context['ChangePass'] = change_password_form

        return render(request, updatePass, context)

    # Update user password and update page
    @login_required(login_url='/not_authorized')
    def Update_details(request):

        context = {'ChangeDetails': ChangeDetails}

        if request.POST:
            change_details_form = ChangeDetails(request.POST)
            
            if change_details_form.is_valid():
                first_name = change_details_form.cleaned_data['first_name']
                last_name = change_details_form.cleaned_data['last_name']
                email = change_details_form.cleaned_data['email']
                phone_number = change_details_form.cleaned_data['phone_number']
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
                context['ChangeDetails'] = change_details_form

        return render(request, updateDetails, context)


# class for handling register functionality
class Register:
    # Render register screen
    def Register_screen(request):
        context = { 'RegForm': RegisterForm }
        return render(request, register, context)

    # Create new user
    def Register_account(request):
        register_form = RegisterForm(request.POST or None)
        
        if request.POST and register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            phone_number = register_form.cleaned_data['phone_number']
            apartment = register_form.cleaned_data['apartment']

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

        return render(request, register, { 'RegForm': register_form })


# class for handling login functionality
class Login:
    # Render login screen
    def Login_screen(request):
        context = {'LogForm': LoginForm }
        return render(request, login, context)

    # Log in for registered users
    def Login_check(request):

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
            LogForm = LoginForm()

        # if invalid form
        return render(request, login, { 'LogForm': LogForm })
    

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
        context = {'ResetForm': PasswordResetRequestForm}
        return render(request, forgot_password, context)

    # reset password view using django built in functionality
    def Reset(request):
        if request.POST:
            reset_form = PasswordResetRequestForm(request.POST)
            
            if not reset_form.is_valid():
                return render(request, forgot_password, {'ResetForm': reset_form})
                
        # Wrap the built-in password reset view and pass it the arguments
        # like the template name, email template name, subject template name
        # and the url to redirect after the password reset is initiated.
        return password_reset(request, template_name=forgot_password,
            email_template_name='account/Password_reset_email.html',
            subject_template_name='account/Password_reset_subject.txt',
            post_reset_redirect='/login',
            extra_context={'ResetForm': PasswordResetRequestForm})

    # display reset confirm view using django built in functionality
    # This view handles password reset confirmation links. See urls.py file for the mapping.
    def Reset_confirm(request, uidb64=None, token=None):
        # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
        # and template name, url to redirect after password reset is confirmed.
        return password_reset_confirm(request, template_name=password_confirm,
            uidb64=uidb64, token=token, post_reset_redirect='/login',
            set_password_form=PasswordChangeForm)