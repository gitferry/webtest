from django.conf.urls import patterns, url

from peni import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='index'),
	url(r'search/$', views.search, name='search'),
)