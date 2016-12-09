from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Parking_space(models.Model):
    number = models.IntegerField(unique=True)
    owner = models.ForeignKey(User)
    
    def __str__(self):
        return "%s - %s %s"%(str(self.number),str(self.owner.first_name),str(self.owner.last_name))

    
class Booking(models.Model):
    space = models.ForeignKey(Parking_space)
    taken = models.BooleanField(default=False)
    start_date = models.DateField()
    stop_date = models.DateField()
    
    def __str__(self):
        return "%s - %s"%(self.space.number, "Taken" if self.taken is True else "Available")
