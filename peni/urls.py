from django.conf.urls import patterns, url

from peni import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='index'),
	url(r'search/$', views.search, name='search'),
	url(r'scan/$', views.bug_scan, name='scan'),
	url(r'sql/$', views.sql_injection, name='sql'),
	url(r'sql/getdb/$', views.sql_getdb, name='sqldb'),
	url(r'sql/getable/$', views.sql_getable, name='sqltable'),
	url(r'sql/getfiles/$', views.sql_getfiles, name='sqlfiles'),
	url(r'bug/$', views.bug_detail, name='bug'),
	url(r'bug/find/$', views.search_bug, name='bugsearch'),
	url(r'bug/getdetail/$', views.find_bug_detail, name='bugdetail'),
	url(r'pwd/$', views.pwd_crack, name='pwdcrack'),
	url(r'pwd/crack/$', views.pwd_get, name='pwdget'),
	url(r'pwd/md5/$', views.md5_crack, name='md5'),
)