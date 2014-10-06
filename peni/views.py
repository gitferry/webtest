from django.shortcuts import render
from func import information_gathering, result
from func import exploit, scan
from models import PortTarget, Port, WebInfo
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import random
import os

def home(request):
	return render(request, 'peni/home.html', {})

def search(request):
	search_url = request.GET['q']
	r = result.result()
	information_gathering.nmap(search_url, r)
	information_gathering.whatweb(search_url, r)
	target = PortTarget()
	target.sys_info = r.operatingsystem
	target.ip = search_url
	target.save()
	for item in r.webinformation:
		info = WebInfo()
		info.target = target
		info.info = item
		info.save()
	for key in r.portservice:
		port = Port()
		port.target = target
		port.number = key
		port.details = r.portservice[key]
		port.save()
	return render(request, 'peni/detail.html', {'target': target})

def scan_wapiti(request, scan_url, r):
	ran = str(random.randint(0, 10000))
	os.makedirs('/home/webtest/peni/static/peni/' + ran + '/')
	scan.wapiti(scan_url, r, '/home/webtest/peni/static/peni/' + ran + '/')
	return HttpResponseRedirect('../../static/peni/' + ran + '/index.html')

def scan_openvas(request, scan_url, r):
	scan.openvas(scan_url, r)
	return HttpResponseRedirect(r.openvas_report)

def scan_wps(request, scan_url, r):
	scan.wpscan(scan_url, r)
	return render(request, 'peni/wpsdetail.html', {'content': r.wpscan_output, 'url': scan_url})

def bug_scan(request):
	scan_url = request.GET['q']
	r = result.result()
	choose = request.GET['id']
	if choose == '1':
		return scan_wapiti(request, scan_url, r)
	elif choose == '2':
		return scan_openvas(request, scan_url, r)
	elif choose == '3':
		return scan_wps(request, scan_url, r)

def sql_getdb(request):
	scan_url = request.GET['q']
	r = result.result()
	exploit.sqlmap_finddbs(scan_url, r)
	dblist = r.sqlmap_dbs
	content = '<table>'
	for db in dblist:
		content += '<tr><td>' + db + '<td/></tr>'
	content += '</table>'
	#return dblist
	#return render(request, 'peni/sqlindex.html', {'dblist': dblist, 'url':scan_url})
	return HttpResponse(content)

def sql_getable(request):
	scan_url = request.GET['q']
	db_name = request.GET['db']
	r= result.result()
	exploit.sqlmap_findtables(scan_url, db_name, r)
	tablelist = r.sqlmap_tables
	content = '<table>'
	for item in tablelist[db_name]:
		content += '<tr><td>' + item + '<td/></tr>'
	content += '</table>'
	return HttpResponse(content)


def sql_injection(request):
	return render(request, 'peni/sqlindex.html', {})

