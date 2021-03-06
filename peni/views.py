from django.shortcuts import render
from func import information_gathering, result
from func import exploit, scan, bruteforce
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
	# ran = str(random.randint(0, 10000))
	ran = 'scan'
	# os.makedirs('/home/webtest/peni/static/peni/' + ran + '/')
	# scan.wapiti(scan_url, r, '/home/webtest/peni/static/peni/' + ran + '/')
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

def sql_getfiles(request):
	scan_url = request.GET['q']
	db_name = request.GET['db']
	table_name = request.GET['table']
	r= result.result()
	exploit.sqlmap_dumptables(scan_url, db_name, table_name, r)
	path_list = r.sqlmap_dumpfiles
	content = '<table>'
	for path in path_list:
		fobj = open(path)
		content += '<tr><td>' + fobj.read().replace('\n', '<br>') + '</td></tr>'
	content += '</table>'
	return HttpResponse(content)

def find_bug_detail(request):
	path = request.GET['q']
	content = '<textarea >' + open(path).read() + '</textarea>'
	return HttpResponse(content)

def search_bug(request):
	param = request.GET['q']
	r = result.result()
	exploit.exploit_db(param, r)
	return render(request, 'peni/bugdetail.html', {'content': r.exploit_db})

def pwd_get(request):
	url = request.GET['q']
	username = request.GET['p']
	r = result.result()
	bruteforce.bruteforce_wordpress(url, username, r)
	return render(request, 'peni/pwdcrack.html', {'pwd': r.bruteforce_wordpress})

def md5_crack(request):
	md5_string = request.GET['q']
	r = result.result()
	bruteforce.md5_crack(md5_string, r)
	return render(request, 'peni/pwdcrack.html', {'md5': r.bruteforce_md5})

def pwd_crack(request):
	return render(request, 'peni/pwdcrack.html', {})

def bug_detail(request):
	return render(request, 'peni/bugdetail.html', {})

def sql_injection(request):
	return render(request, 'peni/sqlindex.html', {})

