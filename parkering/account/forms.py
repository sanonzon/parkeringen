from django import forms
from account.models import User_data
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# dynamic form for displaying extended user model
class UserDataForm(forms.ModelForm):

    class Meta:
        model = User_data
        fields = ('phone_number',)

    widgets = { 
            'phone_number': forms.TextInput(attrs={'placeholder': 'Username'}),
         }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # add custom error messages
        self.fields['phone_number'].error_messages = {'required': 'This field is required'}

# dynamic loginform with custom validation error messages
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
        self.fields['username','password'].error_messages = {'required': 'This field is required'}


# dynamic register form with custom validation error messages
class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

        widgets = { 
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'email': forms.TextInput(attrs={'placeholder': 'E-mail address'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'last name'}),
         }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # add custom error messages
        self.fields['username', 'email', 'first_name', 'last_name', 'password'].error_messages = {'required': 'This field is required'}

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
