from django.conf.urls import url, include
from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.Let_there_be_light, name='Render_all'),
]
