from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^search/', views.results),
    url(r'^ordinary_search/', views.ordinary_search),
    url(r'^advanced_search/', views.advanced_search)
]
