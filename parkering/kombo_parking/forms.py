from django import forms
from kombo_parking.models import Booking, Parking_space
from django.contrib.auth.models import User

class Booking_Form(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = ('space','start_date','stop_date')
