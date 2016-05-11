from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    return render(request, 'newsfocus/index.html', {})

def results(request):
	return render(request, 'newsfocus/results.html', {})

def ordinary_search(request):
    print "12312312321321312321321321"
    keywords = request.POST.get("keywords")
    result = searchByCategory(keywords)
    return JsonResponse(result, safe=False)
