from __future__ import unicode_literals
from datetime import datetime, timedelta
from kombo_parking.models import Booking

def run():

    # fetch all bookings with a stop date older than 31 days
    bookings = Booking.objects.filter(stop_date__lte=datetime.now()-timedelta(days=31))
    
    # delete all bookings from database if there are any
    if bookings.exists():
        for b in bookings:
            print("Deleted: ", b)
            b.delete()



