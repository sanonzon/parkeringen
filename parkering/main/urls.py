from django.conf.urls import url, include
from . import views

app_name = 'main'

urlpatterns = [

	# display index view
    url(r'^$', views.Let_there_be_light, name='Render_all'),

    # display FAQ
    url(r'^faq$', views.FAQ_screen, name='FAQ_screen'),

    # display test view
    url(r'^test$', views.Test, name='Test'),
]
