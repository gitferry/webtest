from django.shortcuts import render

def home(request):
	return render(request, 'peni/home.html', {})

def search(request):
	search_url = request.GET['q']