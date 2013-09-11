from django.conf.urls import patterns, url

from vidlist import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^demo', views.demo, name='demo'),
	url(r'^player', views.player, name='player')
)
