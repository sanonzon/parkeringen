from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django import forms

# this file extends User and contains additional user data.

class Parking_space(models.Model):
    number = models.IntegerField(unique=True)
    owner = models.ForeignKey(User)
    
    def __str__(self):
        return "%s - %s %s"%(str(self.number),str(self.owner.first_name),str(self.owner.last_name))

class User_data(models.Model):
    user = models.OneToOneField(User, unique=True)
    phone_number = models.CharField(max_length=20, blank="True", null=True)


    
class Booking(models.Model):
    space = models.ForeignKey(Parking_space)
    taken = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()
    
    def __str__(self):
        return "%s - %s"%(self.space.number, "Taken" if self.taken is True else "Available")

    

    
