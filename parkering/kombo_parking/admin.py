from django.contrib import admin
from kombo_parking.models import Booking, Parking_space

# Register your models here.


admin.site.register(Booking)
admin.site.register(Parking_space)
