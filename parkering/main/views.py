from django.shortcuts import render

# Render account login/registration page on request
def Let_there_be_light(request):
    return render(request, 'main/base.html')
