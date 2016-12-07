from django.conf.urls import url
from . import views

urlpatterns = [
    # display frontpage content
    url(r'^$', views.Let_there_be_light, name='Render_all'),
]