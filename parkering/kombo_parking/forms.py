from django import forms
from kombo_parking.models import Booking, Parking_space
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget
from datetime import datetime
#~ from django.template import RequestContext
MINUTES = (
    ('00','00'),('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),
    ('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),
    ('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),
    ('30','30'),('31','31'),('32','32'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),
    ('40','40'),('41','41'),('42','42'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),
    ('50','50'),('51','51'),('52','52'),('53','53'),('54','54'),('55','55'),('56','56'),('57','57'),('58','58'),('59','59'),
    )
    
HOURS = (
    ('00','00'),('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),
    ('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),
    ('20','20'),('21','21'),('22','22'),('23','23'),
    )
    
    

class Booking_Form(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ('start_date','stop_date')

#~ def get_spaces(request):
    #~ return Parking_space.objects.filter(owner=request.user.id)


class Space_available_form(forms.Form):
    space = forms.CharField(label='Plats')
    start_date = forms.DateTimeField(label='Start',widget=SelectDateWidget)
    stop_date = forms.DateTimeField(label='Stop',widget=SelectDateWidget)


class Rent_space_form(forms.Form):
    """docstring for Rent_space_form"""

    # Class inheriting ModelChoiceField for minor customizations
    # This won't be used outside of Rent_space_form, thus it is made private
    class _ParkingSpaceModelChoiceField(forms.ModelChoiceField):

        # Overriding label_from_instance function
        def label_from_instance(self, obj):
            return "%s" % obj.number
    
    space = _ParkingSpaceModelChoiceField(
        queryset=Parking_space.objects.none(),
        to_field_name="number",
        empty_label=None)
        
    start_date = forms.DateTimeField(
        label='Start',
        widget=SelectDateWidget)
    start_hour = forms.ChoiceField(
        choices=HOURS)
    start_minute = forms.ChoiceField(
        choices=MINUTES)
        
    stop_date = forms.DateTimeField(
        label='Stop',
        widget=SelectDateWidget)
    stop_hour = forms.ChoiceField(
        choices=HOURS)
    stop_minute = forms.ChoiceField(
        choices=MINUTES)  
        
        
    def __init__(self, user, *args, **kwargs):
        super(Rent_space_form, self).__init__(*args, **kwargs)
        self.fields['space'].queryset = Parking_space.objects.filter(owner=user).order_by('number')
        
    ### description = forms.CharField(label='Beskrivning')
    """ def __init__(self, arg):
        super(Rent_space_form, self).__init__()
        self.arg = arg """
        
    def clean_stop_minute(self):
        #parking_space = self.cleaned_data['space']
        start = self.cleaned_data['start_date']
        stop = self.cleaned_data['stop_date']
        
        start_h = int(self.cleaned_data['start_hour'])
        start_m = int(self.cleaned_data['start_minute'])
        stop_h = int(self.cleaned_data['stop_hour'])
        stop_m = int(self.cleaned_data['stop_minute'])               
        
        if stop < start:
            raise forms.ValidationError(u"Stop date cannot be before start date.")        
        
        elif stop == start:
            if stop_h < start_h:
                raise forms.ValidationError(u"Stop hour cannot be before start hour.")
            elif stop_m < start_m:
                raise forms.ValidationError(u"Stop minute cannot be before start minute.")
        
        #datetime_start = start.replace(hour=start_h, minute=start_m)
        #datetime_stop = stop.replace(hour=stop_h, minute=stop_m)   
        
        # input_start is later than db_start AND input_stop is earlier than db_stop
        #if Booking.objects.filter(space=parking_space, start_date__lte=datetime_start, stop_date__gte=datetime_stop):
        #   raise forms.ValidationError(u"Parking space already rented out within that interval.")
            
        # input_start is later than db_start AND input_stop is earlier than db_stop
        #elif Booking.objects.filter(space=parking_space, start_date__gte=datetime_start, stop_date__lte=datetime_stop):             
        #    raise forms.ValidationError(u"Parking space already rented out within that interval.")
                
        return stop_m    

class Request_space_form(forms.Form):
    """docstring for Request_space_form"""
      
    start_date = forms.DateTimeField(
        label='Start',
        widget=SelectDateWidget)
    start_hour = forms.ChoiceField(
        choices=HOURS)
    start_minute = forms.ChoiceField(
        choices=MINUTES)
        
    stop_date = forms.DateTimeField(
        label='Stop',
        widget=SelectDateWidget) 
    stop_hour = forms.ChoiceField(
        choices=HOURS)
    stop_minute = forms.ChoiceField(
        choices=MINUTES)      
        
    def clean_stop_minute(self):
        start = self.cleaned_data['start_date']
        stop = self.cleaned_data['stop_date']
        
        start_h = int(self.cleaned_data['start_hour'])
        start_m = int(self.cleaned_data['start_minute'])
        stop_h = int(self.cleaned_data['stop_hour'])
        stop_m = int(self.cleaned_data['stop_minute'])
                       
        if stop < start:
            raise forms.ValidationError(u"Stop date cannot be before start date.")        
        
        elif stop == start:
            if stop_h < start_h:
                raise forms.ValidationError(u"Stop hour cannot be before start hour.")
            elif stop_m < start_m:
                raise forms.ValidationError(u"Stop minute cannot be before start minute.")
                
        return stop_m
        
class Request_to_own_Parking_space(forms.Form):
    number = forms.IntegerField(label='Parking space')
    
    def clean_number(self):
        n = self.cleaned_data['number']
        if Parking_space.objects.filter(number=n).exists():
            raise forms.ValidationError(u"Parking space already taken.")
        return n
    
class Unregister_Parking_Space(forms.Form):
    class _ParkingSpaceModelChoiceField(forms.ModelChoiceField):

        # Overriding label_from_instance function
        def label_from_instance(self, obj):
            return "%s" % obj.number
    
    space = _ParkingSpaceModelChoiceField(
        queryset=Parking_space.objects.none(),
        to_field_name="number",
        empty_label=None)      

        
    def __init__(self, user, *args, **kwargs):
        super(Unregister_Parking_Space, self).__init__(*args, **kwargs)
        self.fields['space'].queryset = Parking_space.objects.filter(owner=user).order_by('number')
        
    
    def clean_number(self):
        n = self.cleaned_data['space'].number
        if not Parking_space.objects.filter(owner=user, number=n).exists():
            raise forms.ValidationError(u"You are not the owner of this.")
            
        return n
        
        
        
        