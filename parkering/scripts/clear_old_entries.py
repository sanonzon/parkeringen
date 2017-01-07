from __future__ import unicode_literals
#~ import os, sys
#~ sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#~ import django
#~ os.environ.setdefault("DJANGO_SETTING_MODUL", "parking.settings")
#~ from django.conf import settings
#~ settings.configure()

#~ sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime, timedelta
import dateutil.relativedelta
from kombo_parking.models import Booking

def run():
    d = datetime.now() - dateutil.relativedelta.relativedelta(months=1)
    print datetime.now()
    print d
    
    #~ doot = Booking.objects.filter(stop_date > datetime.now())
    
    #~ for d in doot:
        #~ print d.number




