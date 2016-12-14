from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# extends User and contains additional user data.
class User_data(models.Model):
    user = models.OneToOneField(User, unique=True)
    phone_number = models.CharField(max_length=20)
    apartment = models.CharField(max_length=10)

# allow admin to add apartment numbers for users that may register
class Apartment_number(models.Model):
    apartment_number = models.CharField(max_length=10)

    def __str__(self):
        return self.apartment_number