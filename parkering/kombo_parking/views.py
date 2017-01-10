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
from .forms import Booking_Form,Space_available_form,Rent_space_form,Request_space_form
from django.template import loader
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

def calendar(request):
    #~ print ("\nREQUEST:POST\n%s\n\n" % request.POST) 
    #~ if request.user.is_authenticated():
    if request.is_ajax():        
        #~ print ("AJAX TRIGGERED")
        if request.POST['date']:
            #~ print ("\n\ndateclick event date: %s\n" % request.POST['date'])
            #~ print Booking.objects.filter(start_date__contains(request.POST['date']))
            datelist = Booking.objects.filter(start_date__startswith=request.POST['date'],taken=False)
            requests = Requested_Space.objects.filter(start_date__startswith=request.POST['date'])
            #~ print datelist
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
            #~ print "\n\n%s\n\n" % calendar            
            html = loader.render_to_string('kombo_parking/calendarmodal.html', {
                    'list': calendar,
                    'requests' : request_list,
                    'request_form' : Request_space_form(),
                })
                            
            return HttpResponse(html)
        else:
            html = loader.render_to_string('kombo_parking/calendarmodal.html', {                    
                })
            return HttpResponse(html)
            
    else:
        #~ events = Booking.objects.filter(taken = False).all()
        bookings = Booking.objects.all()

        calendar = []

        if bookings:
            for event in bookings:
                calendar.append({
                    'id':event.id,
                    'number': event.space.number,
                    'start': event.start_date.isoformat(),
                    'stop': event.stop_date.isoformat(),
                })
            return render(request, 'kombo_parking/calendar.html', {
                    'list': calendar,
                })

        return render(request, 'kombo_parking/calendar.html')
    #~ else:
        #~ return redirect("/")

def grab_parkingspace(request):
    if request.is_ajax():
        if request.POST['booking_id']:
            item = Booking.objects.filter(id=int(request.POST['booking_id'])).update(taken=True)
            #~ item.save()

        #~ print Booking.objects.filter(id=int(request.POST['booking_id'])
            #~ html = loader.redirect('kombo_parking/calendar.html')
            return HttpResponse(loader.render_to_string('kombo_parking/calendar.html'))
    else:
        return redirect("/")


def makespaceavailable(request):
    if request.method == 'POST':
        spaces = list(Parking_space.objects.values_list('number',flat=True).filter(owner=request.user.id))

        # create a form instance and populate it with data from the request:
        form = Space_available_form(request.POST)
        #~ print (form)

        #~ print ("nummer: %s\nstart: %s\nStop: %s\n"%(form.space, form.start_date, form.stop_date))


    return redirect('/calender')

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
    rent_space_form = Rent_space_form(request.user)
    context = {'rentout': rent_space_form, 'list': calendar}
    return render(request, 'main/base.html', context)

def rentdetails(request):
    if request.method == 'POST':
        rent_space_form = Rent_space_form(request.user, request.POST)
    
        if rent_space_form.is_valid():
            space = rent_space_form.cleaned_data['space']
            start_date = rent_space_form.cleaned_data['start_date']
            stop_date = rent_space_form.cleaned_data['stop_date']

            booking = Booking()
            booking.space = space
            booking.start_date = start_date
            booking.stop_date = stop_date
            booking.save()

            return redirect('/frontpage')
            #~ return render(request, 'main/base.html', {'rentout': Rent_space_form(request.user)})
            
        return render(request, 'main/base.html', {'rentout': rent_space_form})
    return redirect('/frontpage')
            
    ### call this with action="{%url 'kombo_parking:rentdetails'%}" in template in a html tag?

def request_space(request):
    if request.user.is_authenticated():
        if request.is_ajax():        
            start_fix = "%s %s %s" %( request.POST['start[month]'], request.POST['start[day]'], request.POST['start[year]'] )
            stop_fix = "%s %s %s" %( request.POST['end[month]'], request.POST['end[day]'], request.POST['end[year]'])
            
            datetime_start = datetime.strptime(start_fix, '%B %d %Y')
            datetime_stop = datetime.strptime(stop_fix, '%B %d %Y')
            
            request_space = Requested_Space()
            request_space.renter = request.user            
            request_space.start_date = datetime.date(datetime_start)
            request_space.stop_date = datetime.date(datetime_stop)
          
            request_space.save()
                
    return redirect('/frontpage')
        
        
def rentout_your_space_to_people(request):
    if request.user.is_authenticated():
        if request.is_ajax():   
            requested = Requested_Space.objects.filter(id=request.POST['booking_id']).get()
            spaces = Parking_space.objects.filter(owner=request.user)
            if spaces:
                book = Booking()
                book.owner = requested.renter
                book.taken = True
                book.space = Parking_space.objects.filter(number=spaces[0].number).get()
                book.start_date = requested.start_date
                book.stop_date = requested.stop_date
            
                book.save()
                requested.delete()

    return redirect('/frontpage')
    