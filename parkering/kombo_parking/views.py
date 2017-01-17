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
from .forms import Rent_space_form, Request_space_form, Request_to_own_Parking_space, Unregister_Parking_Space
from django.template import loader
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest


# EmailMessage('Kombo Parking', 'Plats: %s uthyrd' % booking.space.number, to=[booking.space.owner.email]).send()
def send_mail(subject, email_to, body,):
    EmailMessage(subject, body, to=[email_to]).send()
    
def calendar_click(request):
    if request.is_ajax():
        if request.POST['date']:
            booked = Booking.objects.filter(start_date__startswith=request.POST['date'],taken=True)
            datelist = Booking.objects.filter(start_date__startswith=request.POST['date'],taken=False)
            requests = Requested_Space.objects.filter(start_date__startswith=request.POST['date'])

            calendar = []
            request_list = []
            booked_list = []
            
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

            if booked:
                for event in booked:
                    booked_list.append({
                        'id':event.id,
                        'number': event.space.number,
                        'start_date': event.start_date.strftime("%Y-%m-%d %H:%M"),
                        'stop_date': event.stop_date.strftime("%Y-%m-%d %H:%M"),
                        'booked_user_data' : User_data.objects.filter(user=event.owner).get() if User_data.objects.filter(user=event.owner).exists() else None,
                        'booked_user' : User.objects.filter(id=event.owner.id).get(),                        
                    })
                    
            html = loader.render_to_string('kombo_parking/calendarmodal.html', {
                    'list': calendar,
                    'requests' : request_list,
                    'parking_spaces': Parking_space.objects.filter(owner=request.user).values_list('number', flat=True).order_by('number'),
                    'bookings': booked_list, 
                    'request': request,
                    'you_have_booked_spaces': True if Booking.objects.filter(start_date__startswith=request.POST['date'],taken=True).filter(owner=request.user) else False
                    
                })
                            
            return HttpResponse(html)
    else:
        return redirect("/")

def grab_parkingspace(request):
    ''' IF chosen booking is your own, Deletes your booking, making space bookable.
        Else Books parking space for you.
    '''
    if request.is_ajax():
        if request.POST['booking_id']:
            item = Booking.objects.filter(id=int(request.POST['booking_id'])).get()            
                        
            # Remove your available parking space (if you you uploaded wrong info)
            if item.space.owner == request.user and item.taken == False:
                item.delete()
                
                
            else:            
                # Unbook, make it available to others.
                if item.owner == request.user:
                    item.taken = False
                    item.owner = None
                    item.save()
     
                    if item.space.owner.email:
                        subject = "Parking space %s no longer booked" % (item.space.number)
                        email_to = item.space.owner.email
                        start = item.start_date.strftime("%Y-%m-%d %H:%M")
                        stop = item.stop_date.strftime("%Y-%m-%d %H:%M")
                        body = "Parking space %s no longer booked" % (item.space.number)
                        
                        send_mail(subject, email_to, body)
     
                #elif item.space.owner == request.user:
                #    item.delete()
                    
                else:
                    item.owner = request.user
                    item.taken = True        
                    
                    # Send emil to the owner of parking space with info who rented it.
                    if item.space.owner.email:
                        subject = "Parking space rented"
                        email_to = item.space.owner.email
                        start = item.start_date.strftime("%Y-%m-%d %H:%M")
                        stop = item.stop_date.strftime("%Y-%m-%d %H:%M")
                        body = "Parking space %s rented to %s %s from %s to %s\nPhone number: %s" % (item.space.number, request.user.first_name, request.user.last_name, start, stop, User_data.objects.filter(user=request.user).get().phone_number)
                                                
                        send_mail(subject, email_to, body)
                        
                        # Send confirmation email to the user who rented it.
                        subject = "Parking space rented"
                        email_to = request.user.email
                        start = item.start_date.strftime("%Y-%m-%d %H:%M")
                        stop = item.stop_date.strftime("%Y-%m-%d %H:%M")
                        body = "Parking space %s rented.\nDate/time start: %s\nDate/time stop: %s\nOwner phone: %s" % (item.space.number, start, stop, User_data.objects.get(user=item.space.owner).phone_number)
                                                
                        send_mail(subject, email_to, body)
                        
                    
                    
                     
                    item.save()
                
            return HttpResponse(loader.render_to_string('kombo_parking/calendar.html'))
    else:
        return redirect("/")
        
''' Rents out your Parking space to chosen request'''
def rentout_your_space_to_people(request):
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
            
                
                
                if requested.renter.email:
                    subject = "Parking request accepted"
                    email_to = book.owner.email
                    start = book.start_date.strftime("%Y-%m-%d %H:%M")
                    stop = book.stop_date.strftime("%Y-%m-%d %H:%M")
                    body = "Your request to rent a parking space has been accepted by %s %s.\nParking space: %s\nDate/time start: %s\nDate/time stop: %s\nUser contact: %s\n" %(request.user.first_name, request.user.last_name, book.space.number, start, stop, User_data.objects.filter(user=request.user).get().phone_number)
                    
                    send_mail(subject, email_to, body)
                 
                    book.save()
                requested.delete()
            
        except ValueError:
            pass
    return redirect('/')


@login_required(login_url='/not_authorized',redirect_field_name=None)
def calendar(request):   
    ''' START CALENDAR EVENTS '''
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
            
    ''' END CALENDAR EVENTS '''
    
    ''' Init empty forms in case of not request.POST '''
    rent_space_form = Rent_space_form(request.user, None)
    request_form = Request_space_form
    register_parking_space = Request_to_own_Parking_space
    unregister_space_form = Unregister_Parking_Space(request.user, request.POST)
    
    
    
    
    '''
        Beginning of form handlers and request == POST,
        If Form is correct -> Reloads page to avoid double post on Refresh.
    '''    
    if request.method == 'POST':
        ''' Rent-out your space '''
        if 'rentout_parking_space' in request.POST['form_content_check']:
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
                
                return redirect('/calendar')
    

        ''' Request Space Form '''
        if 'request_parking_space' in request.POST['form_content_check']:
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
                
                return redirect('/calendar')
            
        ''' Register Parking Space Form '''
        
        if 'register_for_parking_space' in request.POST['form_content_check']:
            register_parking_space = Request_to_own_Parking_space(request.POST)        
            if register_parking_space.is_valid():
                space_number = register_parking_space.cleaned_data['number']
               
                space = Parking_space()
                space.owner = request.user
                space.number = space_number
            
                space.save()
                
                return redirect('/calendar')
            
        ''' Un-register Parking Space Form '''
        if 'unregister_for_parking_space' in request.POST['form_content_check']:
            unregister_space_form = Unregister_Parking_Space(request.user, request.POST)
            if unregister_space_form.is_valid():
                space_number = unregister_space_form.cleaned_data['space']
                space_number.delete()
                
                return redirect('/calendar')
            
        ''' 
            END of Form handlers 
        '''
     

    ''' If any errors occured: Render those forms with their errors. '''
    context = {
        'rentout': rent_space_form,
        'list': calendar,
        'request_form': request_form,
        'request_parking_space_form': register_parking_space,
        'unregister_space_form': unregister_space_form
    }

    return render(request, 'main/base.html', context)

        
        
   
        
    '''
    else:
        request_form = Request_space_form()
        rent_space_form = Rent_space_form(request.user)        
    
        
        context = {'rentout': rent_space_form, 'list': calendar, 'request_form': request_form, 'request_parking_space_form': Request_to_own_Parking_space,
            'unregister_space_form': Unregister_Parking_Space(request.user)}
        return render(request, 'main/base.html', context)

    '''
