from django.conf.urls import include, url
from . import views

app_name = 'kombo_parking'

urlpatterns = [
    # url(r'^calendar/$', views.frontpage, name='frontpage'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^calendar_click/$', views.calendar_click, name='calendar_click'),
    url(r'^grab_parkingspace/', views.grab_parkingspace),    
    url(r'^rentout_your_space_to_people/$', views.rentout_your_space_to_people, name='rentout_your_space_to_people'),
]
