from django.conf.urls import url
from . import views

app_name = 'reporter'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax-response-chart/$', views.ajax_response_chart, name='ajax_response_chart'),
    url(r'^ajax-response-pie/$', views.ajax_response_pie, name='ajax_response_pie')
]