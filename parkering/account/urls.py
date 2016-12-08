from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [

    # display index screen
	url(r'^$', views.Index_screen, name='Index_screen'),

    # used for login function
	url(r'^login/auth$', views.Login_check, name='Login_check'),

    # used for logout function
	url(r'^logout$', views.Logout, name='Logout'),

    # display login screen
    url(r'^login$', views.Login_screen, name='Login_screen'),

    # display register screen
    url(r'^register$', views.Register_screen, name='Register_screen'),

    # display forgot password view
    url(r'^forgot_password$', views.Forgot_password_screen, name='Forgot_password_screen'),

    # used for register account function
    url(r'^register_account$', views.Register_account, name='Register_account'),

    # display account management
    url(r'^account_management$', views.Account_screen, name='Account_screen'),

    # display not authorized page
    url(r'^not_authorized$', views.Authorization_failed, name='Authorization_failed'),

    # used for update password function
    url(r'^update_password$', views.Update_password, name='Update_password'),

    # the built-in password reset view. The first argument is a
    url(r'^reset_password$', views.reset, name='reset'),
    
    # reset confirmation view, used with the password email reset link.
    url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset_confirm, name='password_reset_confirm'),
]