from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
	url(r'^$', views.Index_screen, name='Index_screen'),
	url(r'^auth$', views.Login_check, name='Login_check'),
	url(r'^logout$', views.Logout, name='Logout'),
    url(r'^login$', views.Login_screen, name='Login_screen'),
    url(r'^register$', views.Register_screen, name='Register_screen'),
    url(r'^forgot_password$', views.Forgot_password_screen, name='Forgot_password_screen'),
    url(r'^register_account$', views.Register_account, name='Register_account'),
    url(r'^account_management$', views.Account_screen, name='Account_screen'),
    url(r'^not_authorized$', views.Authorization_failed, name='Authorization_failed'),
    url(r'^update_password$', views.Update_password, name='Update_password'),

    # here be dragons

    # Map the root URL / to the 'app.hello.reset' view that wraps
    # the built-in password reset view. The first argument is a
    # regular expression that matches the path of the URL after /. Since
    # '^$' matches an empty string, this pattern matches the root URL /.
    url(r'^reset_password$', views.reset, name='reset'),
    
    # Map the 'app.hello.reset_confirm' view that wraps around built-in password
    # reset confirmation view, to the password reset confirmation links.
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset_confirm, name='password_reset_confirm'),

    # end of dragons
]