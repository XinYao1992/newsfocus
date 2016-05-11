from django.shortcuts import render
from django.shortcuts import render_to_response
from search_news import searchByCategory, advanced_search
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'newsfocus/index.html', {})

def results(request):
	keywords = request.POST.get("keywords")
	results = advanced_search(keywords=keywords)
	print "!!!!!!!! ", len(results)
	return render(request, 'newsfocus/results.html', {'results': results})

def ordinary_search(request):
	keywords = request.POST.get("keywords")
	result = searchByCategory(keywords)
	return JsonResponse(result, safe=False)
