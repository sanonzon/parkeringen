from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def Showfullname (request):
    fullname =  request.user.get_full_name()
    context = {'fullname':fullname}
    return render(request, 'main/base.html', context)

# Render account login/registration page on request
def Let_there_be_light(request):
    return render(request, 'main/base.html')

# development page for testing
def Test(request):
    return render(request, 'dev/test.html')


