from django.shortcuts import render
from django.shortcuts import render_to_response
from search_news import searchByCategory, niceSearch
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'newsfocus/index.html', {})

def results(request):
	return render(request, 'newsfocus/results.html', {})

def ordinary_search(request):
    keywords = request.POST.get("keywords")
    result = niceSearch(keywords=keywords)
    return JsonResponse(result, safe=False)

def advanced_search(request):
    keywords = request.POST.get("keywords")
    daterange = request.POST.get("daterange")
    categories = request.POST.getlist("categories[]")
    result = niceSearch(keywords=keywords, ctg=categories)
    return JsonResponse(result, safe=False)
