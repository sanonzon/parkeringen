from django.conf.urls import url
from . import views

app_name = 'account'

urlpatterns = [
	url(r'^$', views.Index_screen, name='Index_screen'),
	url(r'^auth$', views.Login_check, name='Login_check'),
	url(r'^logout$', views.Logout, name='Logout'),
    url(r'^login$', views.Login_screen, name='Login_screen'),
    url(r'^register$', views.Register_screen, name='Register_screen'),
    url(r'^register_account$', views.Register_account, name='Register_account'),
    url(r'^account_management$', views.Account_screen, name='Account_screen'),
    url(r'^not_authorized$', views.Authorization_failed, name='Authorization_failed'),
    url(r'^update_password$', views.Update_password, name='Update_password'),
]
