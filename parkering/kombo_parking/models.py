from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Parking_space(models.Model):
    number = models.IntegerField(unique=True)
    owner = models.ForeignKey(User)
    
    def __str__(self):
        return "%s - %s %s"%(str(self.number),str(self.owner.first_name),str(self.owner.last_name))

    
class Booking(models.Model):
    space = models.ForeignKey(Parking_space)
    owner = models.ForeignKey(User, null=True)
    taken = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()
    
    def clean(self):
        if self.start_date >= self.stop_date:
            raise ValidationError("Stop date cannot be earlier than the start date!")
    
    #~ def save(self, *args, **kwargs):
        #~ if self.owner is None:  # Set default reference
            #~ self.owner = self.space.owner
        #~ super(Booking, self).save(*args, **kwargs)
        
    def __str__(self):
        if self.owner:
            return "%s - %s, %s -> %s booked by %s %s"%(self.space.number, "Taken" if self.taken is True else "Available", self.start_date, self.stop_date, self.owner.first_name, self.owner.last_name)
        else:
            return "Dummyfix, ingen owner"

class Requested_Space(models.Model):
    renter = models.ForeignKey(User)
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()
    
    def clean(self):
        if self.start_date >= self.stop_date:
            raise ValidationError("Stop date cannot be earlier than the start date!")
            
    def __str__(self):
        return "%s Requests space FROM %s TO %s" % (self.renter, self.start_date, self.stop_date)