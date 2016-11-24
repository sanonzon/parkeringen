from django.contrib import admin

from .models import User_Extended
from .models import Parkspace

admin.site.register(User_Extended)
admin.site.register(Parkspace)
