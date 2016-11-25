from django.conf.urls import url
from . import views

app_name = 'account'

urlpatterns = [
	url(r'^$', views.Index, name='Index'),
	url(r'^auth$', views.Login_check, name='Login_check'),
	url(r'^logout$', views.Logout, name='Logout'),
    url(r'^login$', views.Login_screen, name='Login_screen'),
    url(r'^register$', views.Register_screen, name='Register_screen'),
    url(r'^register_account$', views.Register_account, name='Register_account'),
]
