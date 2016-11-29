from django import forms
from account.models import User_data
from django.contrib.auth.models import User

class UserDataForm(forms.ModelForm):

	class Meta:
		model = User_data
		fields = ('phone_number',)

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name')

class PasswordResetRequestForm(forms.Form):
    email_address = forms.CharField(
    	label=(""), 
    	widget=forms.TextInput(attrs={'placeholder': 'Email-address'}),
         max_length=254)

# here be dragons

class PasswordChangeForm(forms.Form):
    password = forms.CharField(
    	label=(""), 
    	widget=forms.TextInput(attrs={'placeholder': 'Password'}),
         max_length=254),
    repeat_password = forms.CharField(
    	label=(""), 
    	widget=forms.TextInput(attrs={'placeholder': 'Repeat password'}),
         max_length=254)

# end of dragons