from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import User_data
from account.forms import UserDataForm
from account.forms import UserForm
from django.contrib.auth import logout


# Note to people messing around with the code: 

# in older version Management within authview/register was named 'management'
# accmanage was renamed to accmanage_regauth along with the url name change from management to Management

# variables to html pages have been altered aswell

# File locations set as variables due to frequent usage
Index = 'account/Index_screen.html'
Login = 'account/Login_screen.html'
Register = 'account/Register_screen.html'
Account_management = 'account/Account_screen.html'

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

# Render login screen
def Register_screen(request):
    return render(request, Register)

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

    print("current password: " + Current_password)
    print("new password: " + New_password)
    print("repeated password: " + Repeat_password)

    Password_valid = request.user.check_password(Current_password)
    if Password_valid:
        if New_password == Repeat_password:
            request.user.set_password(New_password)
            request.user.save()
            return redirect('/logout')
        else:
            return render(request, Account_management)
    else:
        return redirect('/')

"""work in progress below this line"""

# Load forms and account management page, used in register and authview(log in)
"""
    @login_required
    def accmanage_regauth(request):
        user_form = UserForm(instance=request.user)
        user_data_form = UserDataForm(instance=request.user.User_data)

        context = {'user_form': user_form, 'User_data_form': User_data_form}
        return render(request, <add page here>, context)
"""

# Create new user
def Register_account(request):
    Username = request.POST.get('Username', '')
    Password = request.POST.get('Password', '')
    Email = request.POST.get('Email_address', '')
    First_name = request.POST.get('First_name', '')
    Last_name = request.POST.get('Last_name', '')
    Phone_number = request.POST.get('Phone_number', '')
    Parking_number = request.POST.get('Parking_number', '')
    Repeat_password = request.POST.get('Repeat_password', '')

    if request.user.is_authenticated():
        return redirect('/test')
    else:
        if not User.objects.filter(username=Username).exists() and Username != "":
            user = User(username=Username)
            User_Data = User_data(user=user)
            if not User_data.objects.filter(parking_number=Parking_number).exists():
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
                User_Data.parking_number = Parking_number
                User_Data.save()
                user = auth.authenticate(username = Username, password = Password)
                if user:
                    auth.login(request, user)
                    return redirect('/test')
                else:
                    return redirect('/') # TODO: render error page
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
        return redirect('/test')
    else:
        return redirect('/login') # TODO: render login error page

def Logout(request):
    logout(request)
    return redirect('/')
