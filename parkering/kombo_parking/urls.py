from django.conf.urls import include, url
from . import views

urlpatterns = [

    url(r'^calendar/$', views.calendar),
    url(r'^grab_parkingspace/', views.grab_parkingspace),
    #~ url(r'^(?P<slug>[-w]+)/$', 'hepsi', name = "hepsiliste")
    url(r'^makespaceavailable/$', views.makespaceavailable, name='makespaceavailable'),

]
