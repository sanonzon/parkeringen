from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Render account login/registration page on request
def Let_there_be_light(request):
    # return render(request, 'main/base.html')
    if request.user.is_authenticated():
        return redirect("/frontpage")
    else:
        return redirect("/")

# render FAQ page on request
def FAQ_screen(request):
    return render(request, 'main/information/FAQ_screen.html')

# development page for testing
def Test(request):
    return render(request, 'dev/test.html')


