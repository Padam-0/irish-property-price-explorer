from django.conf.urls import url
from . import views

app_name = 'riskdb'
urlpatterns = [
    url(r'^$', views.index, name='index')
]