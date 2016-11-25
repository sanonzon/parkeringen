from django.conf.urls import url
from . import views

app_name = 'account'

urlpatterns = [
	url(r'^$', views.Index, name='Index'),
	url(r'^login$', views.Login_check, name='Login_check'),
	url(r'^redirect$', views.Redirect_login, name='Redirect_login'),
    url(r'^login$', views.Login_screen, name='Login_screen'),
    url(r'^register$', views.Register_screen, name='Register_screen'),
]
