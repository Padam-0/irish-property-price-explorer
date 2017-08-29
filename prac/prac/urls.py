from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('homepage.urls', namespace="homepage")),
    url(r'^reporter/', include('reporter.urls', namespace='reporter')),
    url(r'^hp-predictor/', include('predictor.urls', namespace='predictor')),
    url(r'^risk/', include('riskdb.urls', namespace='riskdb')),
    url(r'^table/', include('tableview.urls', namespace='tableview'))
]
