from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import User_data
from .models import Booking
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse
# Create your views here.

def Bookthatspace(request, bookid):
    booking = Booking.objects.filter(id=bookid,taken=False).get()
    print bookid
    if booking:
        booking.taken=True
        booking.save()
    return redirect('/calender')

def Calender(request):
    bookings = Booking.objects.filter(taken=False)
    
    return render(request,'kombo_parking/calender.html', {'bookings':bookings})
