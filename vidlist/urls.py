from django.conf.urls import patterns, url

from vidlist import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^player', views.player, name='player')
)
