from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Render account login/registration page on request
def Let_there_be_light(request):
    return render(request, 'main/base.html')

# development page for testing
def frontpage(request):
    return render(request, 'main/base.html')
