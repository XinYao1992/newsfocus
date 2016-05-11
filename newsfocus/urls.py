from django.conf.urls import url
from newsfocus.views import results
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^search/$', results.as_view(), name='results'),
	url(r'^ordinary_search/', views.ordinary_search),
	url(r'^advanced_search/', views.advanced_search)
]
