from django.conf.urls import url
from . import views

app_name = 'hp-predictor'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax-post-prediction/$', views.predict, name='predict')
]