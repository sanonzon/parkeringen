from django.conf.urls import include, url
from . import views

app_name = 'kombo_parking'

urlpatterns = [
    url(r'^frontpage', views.frontpage, name='frontpage'),
    #~ url(r'^frontpage/error', views.rentdetails, name='rentdetails'),
    url(r'^rentdetails', views.rentdetails, name='rentdetails'),
    url(r'^calendar/$', views.calendar),
    url(r'^grab_parkingspace/', views.grab_parkingspace),    
    url(r'^request_space/$', views.request_space, name='request_space'),
    url(r'^rentout_your_space_to_people/$', views.rentout_your_space_to_people, name='rentout_your_space_to_people'),
    url(r'^register_for_parking_space/$', views.register_for_parking_space, name='register_for_parking_space'),
    url(r'^unregister_for_parking_space/$', views.unregister_for_parking_space, name='unregister_for_parking_space'),
]
