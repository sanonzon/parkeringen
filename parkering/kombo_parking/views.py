from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import User_data
from .models import Booking, Parking_space
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse
from .forms import Booking_Form,Space_available_form
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
    print request.user.id
    spaces = list(Parking_space.objects.values_list('number',flat=True).filter(owner=request.user.id))
    print spaces
    
    return render(request,'kombo_parking/calender.html',
        {
        'bookings':bookings,
         'spaces':spaces,
         'booking_form':Space_available_form,
         })

def makespaceavailable(request):
    ## TODO, form hantering
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Space_available_form(request.POST)
        print form
        
        print "nummer: %s\nstart: %s\nStop: %s\n"%(form.space, form.start_date, form.stop_date)
        
    
    return redirect('/calender')
