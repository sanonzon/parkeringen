from django import forms
from account.models import User_data, Apartment_number
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.core.validators import RegexValidator

minimum_password_length = 8

# dynamic loginform
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    # remove when no longer required
    # access to this but no validation error is displayed in html, with or without tags
    # can be accessed by print(<form>.errors) in views.py
    def clean_password(self):
        cleaned_username = self.cleaned_data['username']
        cleaned_password = self.cleaned_data['password']

        user = auth.authenticate(username = cleaned_username, password = cleaned_password)

        if user is not None:
            if not user.is_active:
                raise forms.ValidationError(u"This account has been inactivated.")
        else:
            raise forms.ValidationError(u"Incorrect login, please try again or register an account.")

        return cleaned_password
        
# cool register form
class RegisterForm(forms.Form):
    
    alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only the letters A to Z and numbers are allowed.')
    phone_number_validator = RegexValidator(r'^(\+[0-9]{4}|0?[0-9]{3})(\ |\-)?([0-9]{1,2})(\ |\-)?([0-9]{1,2})(\ |\-)?([0-9]{1,3})$', 'The phone number entered is not valid.')
    
    username = forms.CharField(
        min_length=3,
        validators=[alphanumeric_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First name'}))

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail address'}))

    password = forms.CharField(
        min_length=minimum_password_length,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    password_repeat = forms.CharField(
        min_length=minimum_password_length,
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    phone_number = forms.CharField(
        validators=[phone_number_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'}))

    apartment = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment number'}))
    
    def clean_username(self):
        cleaned_username = self.cleaned_data['username']
        
        if User.objects.filter(username=cleaned_username).exists():
            raise forms.ValidationError(u"The username %s is already taken." % cleaned_username)
            
        return cleaned_username

    def clean_password_repeat(self):
        #Check if the password was repeated, and if the repeated password is a match.
        cleaned_password = self.cleaned_data.get('password')
        cleaned_password_repeat = self.cleaned_data['password_repeat']

        if not cleaned_password_repeat:
            raise forms.ValidationError(u"Please repeat the password.")
        if cleaned_password != cleaned_password_repeat:
            raise forms.ValidationError(u"The passwords do not match.")
            
        return cleaned_password_repeat

    def clean_apartment(self):
        cleaned_apartment = self.cleaned_data['apartment']
        
        if User_data.objects.filter(apartment=cleaned_apartment).exists():
            raise forms.ValidationError(u"This apartment is already in use.")
            
        if not Apartment_number.objects.filter(apartment_number=cleaned_apartment).exists():
            raise forms.ValidationError(u"This apartment does not exist.")
            
        return cleaned_apartment

class ChangePassword(forms.Form):
    current_password = forms.CharField(label=(""), widget=forms.PasswordInput(attrs={'placeholder': 'Current password'}))
    password = forms.CharField(label=(""), widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    repeat_password = forms.CharField(label=(""), widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))


class ChangeDetails(forms.Form):
    email = forms.EmailField(label=(""), widget=forms.TextInput(attrs={'placeholder': 'Email address'}))
    first_name = forms.CharField(label=(""), widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label=(""), widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    phone_number = forms.CharField(label=(""), widget=forms.TextInput(attrs={'placeholder': 'Phone number'}))

    # extra validation through django native
    def __init__(self, *args, **kwargs):
        super(ChangeDetails, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


# used for forgot password email view
# remove if no longer required
class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail adress'}),
        max_length=254)

    def clean_email(self):
        cleaned_email = self.cleaned_data['email']
        
        if not User.objects.filter(email=cleaned_email).exists():
            raise forms.ValidationError(u"No user related to this e-mail adress found.")
            
        return cleaned_email

# used for forgot password email link view
# remove if no longer required
class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        max_length=254,
        min_length=minimum_password_length)
         
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}),
        max_length=254,
        min_length=minimum_password_length)
        
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        
    def clean_password_repeat(self):
        #Check if the password was repeated, and if the repeated password is a match.
        cleaned_password = self.cleaned_data.get('password')
        cleaned_password_repeat = self.cleaned_data['password_repeat']

        if not cleaned_password_repeat:
            raise forms.ValidationError(u"Please repeat the password.")
        if cleaned_password != cleaned_password_repeat:
            raise forms.ValidationError(u"The passwords do not match.")
            
        return cleaned_password_repeat

    def save(self, commit=True):
        password = self.cleaned_data["password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
