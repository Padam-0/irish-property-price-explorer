from django.conf.urls import url
from . import views

app_name = 'homepage'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax-response-markers/$', views.return_response_markers,
        name='return_response_markers'),
    url(r'^ajax-response-infowindow/$', views.return_response_infowindow,
        name='return_response_infowindow'),
    url(r'^ajax-response-stats/$', views.return_response_stats,
        name='return_response_stats'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^privacy-cookies$', views.legal, name='legal'),
    url(r'^our-data$', views.data, name='data'),
    url(r'^ajax-post-error/', views.write_error, name='write_error')
]