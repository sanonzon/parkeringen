from __future__ import unicode_literals
#~ import os, sys
#~ sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#~ import django
#~ os.environ.setdefault("DJANGO_SETTING_MODUL", "parking.settings")
from django.conf import settings


#~ sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime, timedelta
import dateutil.relativedelta
from kombo_parking.models import Booking

def run():
    old_shit = datetime.now() - dateutil.relativedelta.relativedelta(months=1)
    bokningar = Booking.objects.exclude(stop_date__gt=old_shit)
    
    for b in bokningar:
        print(b.number)
    
    # print datetime.now()
    # print d
    
    #~ doot = Booking.objects.filter(stop_date > datetime.now())
    
    #~ for d in doot:
        #~ print d.number




