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
Logreg = 'account/Logreg.html'
Login = 'account/Login_screen.html'
Register = 'account/Register_screen.html'



# Render account login/registration page on request
def Index(request):
    return render(request, Logreg)

# Render login screen
def Login_screen(request):
    return render(request, Login)

# Render login screen
def Register_screen(request):
    return render(request, Register)

# Update user password and update page
"""@login_required
def update_password(request):
    current_password = request.POST.get('current_password', '')
    new_password = request.POST.get('new_password', '')
    repeat_password = request.POST.get('repeat_password', '')

    password_valid = request.user.check_password(current_password)
    if password_valid:
        if new_password == repeat_password:
            request.user.set_password(new_password)
            request.user.save()
            return render(request, logreg_updatepass)
        else:
            return render(request, account_error)
    else:
        return render(request, account_error)"""

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


"""def logout_view(request):
    logout(request)
    return render(request, logreg)"""

# Create new user
"""def Register(request):
    Username = request.POST.get('Username', '')
    Password = request.POST.get('Password', '')
    Email = request.POST.get('Email_address', '')
    First_name = request.POST.get('First_name', '')
    Last_name = request.POST.get('Last_name', '')
    Phone_number = request.POST.get('Phone_number', '')
    Parking_number = request.POST.get('Parking_number', '')
    Repeat_password = request.POST.get('Repeat_password', '')

    if request.user.is_authenticated():
        return redirect(Login)
    else:
        if not User.objects.filter(username=username).exists() and username != "":
            User = User(username=username)
            User.email = Email
            if Password == Repeat_password and Password != "":
                User.set_password(Password)
            else:
                return render(request, Logreg)
            User.is_active = True
            User.save()
            Userdata = User_data(user=User)
            Userdata.save()
            return render(request, Logreg)
        else:
            return render(request, Logreg)"""

# Log in for registered users
def Login_check(request):
    Username = request.POST.get('Username', '')
    Password = request.POST.get('Password', '')
    print(Username)
    print(Password)

    user = auth.authenticate(username = Username, password = Password)
    if user:
        auth.login(request, user)
        return render(request,Register) # TODO: add redirect here
        #return redirect('Redirect_login')
    else:
        return render(request, Login) # TODO: add error redirect here

# Log in for registered users
def Redirect_login(request):
    return render(request, Register)
