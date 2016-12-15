from django import forms
from kombo_parking.models import Booking, Parking_space
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget
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
    #space = forms.CharField(label='Plats')
    start_date = forms.DateTimeField(label='Start', widget=SelectDateWidget)
    stop_date = forms.DateTimeField(label='Stop', widget=SelectDateWidget)
    ### description = forms.CharField(label='Beskrivning')
    """ def __init__(self, arg):
        super(Rent_space_form, self).__init__()
        self.arg = arg """

