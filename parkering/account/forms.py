from django import forms
from account.models import User_data
from django.contrib.auth.models import User

class UserDataForm(forms.ModelForm):

	class Meta:
		model = User_data
		fields = ('date_of_birth', 'parking_number', 'phone_number')

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name')