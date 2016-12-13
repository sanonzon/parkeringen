from django.conf.urls import include, url
from . import views

app_name = 'kombo_parking'

urlpatterns = [
    url(r'^calendar/$', views.calendar),
    url(r'^grab_parkingspace/', views.grab_parkingspace),
    url(r'^makespaceavailable/$', views.makespaceavailable, name='makespaceavailable'),
]
