from django import forms
from account.models import User_data, Booking, Parking_space
from django.contrib.auth.models import User

class UserDataForm(forms.ModelForm):

	class Meta:
		model = User_data
		fields = ('phone_number',)

class UserForm(forms.ModelForm):
    
	class Meta:
		model = User
		fields = ('first_name', 'last_name')

class Booking_Form(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = ('space','start_date','stop_date')
