from django import forms
from kombo_parking.models import Booking, Parking_space
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget
from datetime import datetime
#~ from django.template import RequestContext



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
        
    stop_date = forms.DateTimeField(
        label='Stop',
        widget=SelectDateWidget)
    
    def __init__(self, user, *args, **kwargs):
        super(Rent_space_form, self).__init__(*args, **kwargs)
        self.fields['space'].queryset = Parking_space.objects.filter(owner=user)
        
    ### description = forms.CharField(label='Beskrivning')
    """ def __init__(self, arg):
        super(Rent_space_form, self).__init__()
        self.arg = arg """

class Request_space_form(forms.Form):
    """docstring for Request_space_form"""
      
    start_date = forms.DateTimeField(
        label='Start',
        widget=SelectDateWidget)
        
    stop_date = forms.DateTimeField(
        label='Stop',
        widget=SelectDateWidget)   
        
        
class Request_to_own_Parking_space(forms.Form):
    number = forms.IntegerField(label='Parking space')
    
    
    
    
