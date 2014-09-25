from django.shortcuts import render
from func import information_gathering, result
from models import PortTarget, Port

def home(request):
	return render(request, 'peni/home.html', {})

def search(request):
	search_url = request.GET['q']
	r = result.result()
	information_gathering.nmap(search_url, r)
	target = PortTarget()
	target.sys_info = r.operatingsystem
	target.ip = search_url
	for key in r.portservice:
		port = Port()
		port.target = target.pk
		port.number = key
		port.details = r.portservice[key]
	return render(request, 'peni/portdetail.html', {'target': target})
