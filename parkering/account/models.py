from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django import forms

# this file extends User and contains additional user data.

class User_data(models.Model):
    user = models.OneToOneField(User, unique=True)
    phone_number = models.CharField(max_length=20, blank="True", null=True)
