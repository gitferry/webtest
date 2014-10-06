from django.conf.urls import patterns, url

from peni import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='index'),
	url(r'search/$', views.search, name='search'),
	url(r'scan/$', views.bug_scan, name='scan'),
	url(r'sql/$', views.sql_injection, name='sql'),
	url(r'sql/getdb/$', views.sql_getdb, name='sqldb'),
)