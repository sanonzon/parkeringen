from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django import forms

# this file extends User and contains additional user data.

class User_data(models.Model):
    user = models.OneToOneField(User, unique=True)
    date_of_birth = models.DateField(blank="True", null=True)
    parking_number = models.CharField(max_length=20, blank="True", null=True)
    phone_number = models.CharField(max_length=20, blank="True", null=True)