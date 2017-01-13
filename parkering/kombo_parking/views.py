from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from account.models import User_data
from .models import Booking, Parking_space, Requested_Space
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse
from .forms import Booking_Form,Space_available_form,Rent_space_form, Request_space_form, Request_to_own_Parking_space
from django.template import loader
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

# Function to tryparse integers
def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def calendar(request):
    ''' Onlick-event for events and days in the calendar. Renders the events for specific day.  '''
    #~ if request.user.is_authenticated():
    if request.is_ajax():        
        if request.POST['date']:
            datelist = Booking.objects.filter(start_date__startswith=request.POST['date'],taken=False)
            requests = Requested_Space.objects.filter(start_date__startswith=request.POST['date'])

            calendar = []
            request_list = []
            
            if requests:
                for event in requests:
                    request_list.append({
                        'id':event.id,                        
                        'start_date': event.start_date.strftime("%Y-%m-%d %H:%M"),
                        'stop_date': event.stop_date.strftime("%Y-%m-%d %H:%M"),
                    })               
            
            if datelist:
                for event in datelist:
                    calendar.append({
                        'id':event.id,
                        'number': event.space.number,
                        'start_date': event.start_date.strftime("%Y-%m-%d %H:%M"),
                        'stop_date': event.stop_date.strftime("%Y-%m-%d %H:%M"),
                    })

            html = loader.render_to_string('kombo_parking/calendarmodal.html', {
                    'list': calendar,
                    'requests' : request_list,
                    'parking_spaces': Parking_space.objects.filter(owner=request.user).values_list('number', flat=True).order_by('number'),
                   
                })
                            
            return HttpResponse(html)
        else:
            html = loader.render_to_string('kombo_parking/calendarmodal.html', {                    
                })
            return HttpResponse(html)
            
    else:        
        return redirect("/frontpage")

def grab_parkingspace(request):
    ''' Books parking space if user already owns the space, otherwise deletes the space from being bookable'''
    if request.is_ajax():
        if request.POST['booking_id']:
            item = Booking.objects.filter(id=int(request.POST['booking_id'])).get()
            
            if item.space.owner == request.user:
                item.delete()
                
            else:
                item.owner = request.user
                item.taken = True            
                item.save()

        #~ print Booking.objects.filter(id=int(request.POST['booking_id'])
            #~ html = loader.redirect('kombo_parking/calendar.html')
            return HttpResponse(loader.render_to_string('kombo_parking/calendar.html'))
    else:
        return redirect("/frontpage")


@login_required(login_url='/login')
def frontpage(request):
    bookings = Booking.objects.all()
    calendar = []

    requests = Requested_Space.objects.all()
    if requests:
        for event in requests:
            calendar.append({
                'id':event.id,
                'start': event.start_date.isoformat(),
                'stop': event.stop_date.isoformat(),
                'color': 'orange',
            })
    if bookings:
        for event in bookings:
            calendar.append({
                'id':event.id,
                'number': event.space.number,
                'start': event.start_date.isoformat(),
                'stop': event.stop_date.isoformat(),
                'color': 'red' if event.taken else 'green',            
            })
    rent_space_form = None
    
    request_form = Request_space_form()
    if request.user.is_authenticated():
        rent_space_form = Rent_space_form(request.user)        
    context = {'rentout': rent_space_form, 'list': calendar, 'request_form': request_form, 'request_parking_space_form': Request_to_own_Parking_space  }
    return render(request, 'main/base.html', context)

def rentdetails(request):
    if request.method == 'POST':
        rent_space_form = Rent_space_form(request.user, request.POST)
    
        if rent_space_form.is_valid():
            space = rent_space_form.cleaned_data['space']
            
            start_date = rent_space_form.cleaned_data['start_date']
            start_h = int(rent_space_form.cleaned_data['start_hour'])
            start_m = int(rent_space_form.cleaned_data['start_minute'])
                            
            stop_date = rent_space_form.cleaned_data['stop_date']
            stop_h = int(rent_space_form.cleaned_data['stop_hour'])
            stop_m = int(rent_space_form.cleaned_data['stop_minute'])
            
            fixed_start = start_date.replace(hour=start_h, minute=start_m)
            fixed_stop = stop_date.replace(hour=stop_h, minute=stop_m)     

            booking = Booking()
            booking.space = space
            booking.start_date = fixed_start
            booking.stop_date = fixed_stop
            booking.save()

            return redirect('/frontpage')
            #~ return render(request, 'main/base.html', {'rentout': Rent_space_form(request.user)})
            
        #return render(request, 'main/base.html', {'rentout': rent_space_form})
    return redirect('/frontpage')
            
    ### call this with action="{%url 'kombo_parking:rentdetails'%}" in template in a html tag?

def request_space(request):
    if request.user.is_authenticated():
        if request.POST:
            request_form = Request_space_form(request.POST)
            
    
            if request_form.is_valid():                
                start_date = request_form.cleaned_data['start_date']
                start_h = int(request_form.cleaned_data['start_hour'])
                start_m = int(request_form.cleaned_data['start_minute'])
                                
                stop_date = request_form.cleaned_data['stop_date']
                stop_h = int(request_form.cleaned_data['stop_hour'])
                stop_m = int(request_form.cleaned_data['stop_minute'])
                
                fixed_start = start_date.replace(hour=start_h, minute=start_m)
                fixed_stop = stop_date.replace(hour=stop_h, minute=stop_m)                               
                
                request_space = Requested_Space()
                request_space.renter = request.user            
                request_space.start_date = fixed_start
                request_space.stop_date = fixed_stop
              
                request_space.save()
                
    return redirect('/frontpage')
        
        
def rentout_your_space_to_people(request):
    if request.user.is_authenticated():
        if request.is_ajax():   
            requested = Requested_Space.objects.filter(id=request.POST['booking_id']).get()
            spaces = Parking_space.objects.values_list('number', flat=True).filter(owner=request.user)
                       
            try:
                try_number = int(request.POST['space'])
                if try_number in spaces:
                    book = Booking()
                    book.owner = requested.renter
                    book.taken = True
                    book.space = Parking_space.objects.filter(number=try_number).get()
                    book.start_date = requested.start_date
                    book.stop_date = requested.stop_date
                
                    book.save()
                    requested.delete()
                
            except ValueError:
                pass
    return redirect('/frontpage')
    
    
def register_for_parking_space(request):
    if request.user.is_authenticated():
        if request.POST:
            request_form = Request_to_own_Parking_space(request.POST)
            if request_form.is_valid():
                space_number = request_form.cleaned_data['number']
               
                space = Parking_space()
                space.owner = request.user
                space.number = space_number
            
                space.save()
        
    return redirect("/frontpage")