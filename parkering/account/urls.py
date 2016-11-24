from django.conf.urls import url
from . import views

app_name = 'account'

urlpatterns = [
    url(r'^login$', views.Login_screen, name='Login_screen'),
    url(r'^register$', views.Register_screen, name='Register_screen'),
]
