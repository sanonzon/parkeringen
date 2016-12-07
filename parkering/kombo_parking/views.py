from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def Let_there_be_light(request):
    return render(request, 'main/body.html')
