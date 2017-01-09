from django.conf.urls import include, url
from . import views

app_name = 'kombo_parking'

urlpatterns = [
    url(r'^frontpage', views.frontpage, name='frontpage'),
    #~ url(r'^frontpage/error', views.rentdetails, name='rentdetails'),
    url(r'^rentdetails', views.rentdetails, name='rentdetails'),
    url(r'^calendar/$', views.calendar),
    url(r'^grab_parkingspace/', views.grab_parkingspace),
    url(r'^makespaceavailable/$', views.makespaceavailable, name='makespaceavailable'),
    url(r'^request_space/$', views.request_space, name='request_space'),
]
