from django import forms
from account.models import User_data
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

# dynamic form for extended user model
class UserDataForm(forms.ModelForm):

    class Meta:
        model = User_data
        fields = ('phone_number','apartment')

        widgets = { 
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'apartment': forms.TextInput(attrs={'placeholder': 'Apartment number'}),
        }


# dynamic loginform
class LoginForm(forms.Form):
    username = forms.CharField(
        label=(""), 
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    password = forms.CharField(
        label=(""), 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    # remove when no longer required
    # access to this but no validation error is displayed in html, with or without tags
    # can be accessed by print(<form>.errors) in views.py
    def clean_password(self):
        #cleaned_data = self.cleaned_data
        cleaned_username = self.cleaned_data['username']
        cleaned_password = self.cleaned_data['password']

        user = auth.authenticate(username = cleaned_username, password = cleaned_password)
        if not user:
            raise forms.ValidationError("Incorrect login, please try again or register an account.")
        return cleaned_password


# dynamic register form
class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

        widgets = { 
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail address'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'last name'}),
         }

    # extra validation through django native
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True


# used for forgot password email view
# remove if no longer required
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
