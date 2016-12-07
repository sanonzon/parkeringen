from django import forms
from account.models import User_data
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# modelforms for displaying / accessing extended user model
class UserDataForm(forms.ModelForm):

	class Meta:
		model = User_data
		fields = ('phone_number',)

# remove if not required
class LoginForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username', 'password']

		widgets = { 
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
         }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # add custom error messages
        self.fields['username'].error_messages = {'required': 'This field is required'}

# her be dragons
"""
# login form
class LoginForm(forms.Form):
    # username field
    username = forms.CharField(
        label=(""), 
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
         max_length=254, validators=[validate_username_unique])

    # password field
    password = forms.CharField(
        label=(""), 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
         max_length=254)
"""

# here be dragons

# used for forgot password email view
class PasswordResetRequestForm(forms.Form):
    email_address = forms.CharField(
    	label=(""), 
    	widget=forms.TextInput(attrs={'placeholder': 'Email-address'}),
         max_length=254)

# used for forgot password email link view
# remove if no longer required
class PasswordChangeForm(forms.Form):
    password = forms.CharField(
    	label=(""), 
    	widget=forms.TextInput(attrs={'placeholder': 'Password'}),
         max_length=254),
    repeat_password = forms.CharField(
    	label=(""), 
    	widget=forms.TextInput(attrs={'placeholder': 'Repeat password'}),
         max_length=254)
