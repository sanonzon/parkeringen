from django.contrib import admin
from kombo_parking.models import Booking, Parking_space, Requested_Space

# Register your models here.


admin.site.register(Booking)
admin.site.register(Parking_space)
admin.site.register(Requested_Space)
