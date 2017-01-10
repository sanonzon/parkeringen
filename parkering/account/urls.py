from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [

    # display index screen
	url(r'^$', views.Index.Index_screen, name='Index_screen'),

    # used for login function
	url(r'^login/auth$', views.Login.Login_check, name='Login_check'),

    # used for logout function
	url(r'^logout$', views.Logout.Logout, name='Logout'),

    # display login screen
    url(r'^login$', views.Login.Login_screen, name='Login_screen'),

    # display register screen
    url(r'^register$', views.Register.Register_screen, name='Register_screen'),

    # display forgot password view
    url(r'^forgot_password$', views.ForgotPassword.Forgot_password_screen, name='Forgot_password_screen'),

    # used for register account function
    url(r'^register_account$', views.Register.Register_account, name='Register_account'),

    # display account management
    url(r'^account_management$', views.AccountManagement.Account_screen, name='Account_screen'),

    # display not authorized page
    url(r'^not_authorized$', views.Error.Authorization_failed, name='Authorization_failed'),

    # display update password page
    url(r'^update_password$', views.AccountManagement.UpdatePass_screen, name='UpdatePass_screen'),

    # used for update password function
    url(r'^update_password/update$', views.AccountManagement.Update_password, name='Update_password'),

    # display update password page
    url(r'^update_details$', views.AccountManagement.UpdateDetails_screen, name='UpdateDetails_screen'),

    # display update password page
    url(r'^update_details/update$', views.AccountManagement.Update_details, name='Update_details'),

    # the built-in password reset view.
    url(r'^reset_password$', views.ForgotPassword.Reset, name='reset'),
    
    # reset confirmation view, used with the password email reset link.
    url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ForgotPassword.Reset_confirm, name='password_reset_confirm'),
]