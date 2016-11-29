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

class Parking_space(models.Model):
    number = models.IntegerField(unique=True)
    owner = models.ForeignKey(User)
    
    
class Booking(models.Model):
    space = models.ForeignKey(Parking_space)
    taken = models.BooleanField()
    start_date = models.DateField()
    stop_date = models.DateField()
    
    

    
