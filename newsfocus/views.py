from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from search_news import search_by_category, search_by_all
from django.http import JsonResponse
from django.views.generic import View

# Create your views here.
class results(View):
	def get(self, request, *args, **kwargs):
		category = request.GET.get('category', '')
		results = search_by_category(ctg=category)
		return render(request, 'newsfocus/results.html', {'results': results})

	def post(self, request, *args, **kwargs):
		keywords = request.POST.get('keywords')
		categories = request.POST.getlist('categories')
		daterange = request.POST.get('daterange')
		results = search_by_all(keywords=keywords, ctg=categories, daterange=daterange)
		return render(request, 'newsfocus/results.html', {'results': results})

def index(request):
	lst = ['art', 'business', 'food', 'health', 'science', 'travel', 'sports', 'world']
	return render(request, 'newsfocus/index.html', {'name_lst': lst})

def ordinary_search(request):
	keywords = request.POST.get("keywords")
	result = search_by_all(keywords=keywords)
	return JsonResponse(result, safe=False)

def advanced_search(request):
	keywords = request.POST.get("keywords")
	daterange = request.POST.get("daterange")
	categories = request.POST.getlist("categories[]")
	result = search_by_all(keywords=keywords, ctg=categories, daterange=daterange)
	return JsonResponse(result, safe=False)
