from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    return render(request, 'newsfocus/index.html', {})

def results(request):
	return render(request, 'newsfocus/results.html', {})
