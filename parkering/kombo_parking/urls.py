from django.conf.urls import url, include
from . import views

app_name = 'main'

urlpatterns = [

    # display index view
    url(r'^$', views.Let_there_be_light, name='Render_all'),

    # display test view
    url(r'^frontpage$', views.frontpage, name='frontpage'),
]
