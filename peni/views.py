from django.shortcuts import render
from func import information_gathering, result
from func import exploit, scan
from models import PortTarget, Port, WebInfo
from django.http import HttpResponseRedirect
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

def bug_scan(request):
	scan_url = request.GET['q']
	r = result.result()
	ran = str(random.randint(0, 10000))
	os.makedirs('/home/penetration/webtest/peni/static/peni/' + ran + '/')
	scan.wapiti(scan_url, r, '/home/penetration/webtest/peni/static/peni/' + ran + '/')
	return HttpResponseRedirect('../../static/peni/' + ran + '/generated_report/index.html')