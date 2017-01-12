from __future__ import unicode_literals
from django.conf import settings
from datetime import datetime, timedelta
import dateutil.relativedelta
from kombo_parking.models import Booking

def run():
    old_bookings = datetime.now() - dateutil.relativedelta.relativedelta(months=1)
    bookings = Booking.objects.exclude(stop_date__gt=old_bookings)
    
    if bookings.exists():
    	for b in bookings:
       		b.delete()



