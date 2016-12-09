from django.conf.urls import include, url
from . import views

urlpatterns = [

    url(r'^$', views.Calender, name='Calender'),
    #~ url(r'^(?P<slug>[-w]+)/$', 'hepsi', name = "hepsiliste")
    url(r'^bookthatspace/(?P<bookid>[\d]+)$', views.Bookthatspace, name='Bookthatspace'),
    url(r'^makespaceavailable/$', views.makespaceavailable, name='makespaceavailable'),
    

]
