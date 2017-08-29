from django.conf.urls import url
from . import views

app_name = 'tableview'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax-response-table/$', views.ajax_response_table, name='ajax_response_table'),
    url(r'^ajax-response-map/$', views.ajax_response_map, name='ajax_response_map'),
]