# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from getmusic import getvideos, Song
from django.template.response import TemplateResponse
import simplejson

def index(request):
	subreddits = []
	subreddit = request.GET.get('s','progmetal')
	limit = request.GET.get('l', '200')
	subreddits.append(subreddit)
	playlist = getvideos(subreddits, int(limit))
	template = loader.get_template('vidlist/index.html')
	context = RequestContext(request, {
		'playlist': playlist,
	})
	return HttpResponse(template.render(context))

def player(request):
	subreddits = []
	response_list = []
	if not request.POST:
		subreddit = request.GET.get('s','jazz')
		limit = request.GET.get('l', '20')
		subreddits.append(subreddit)
		playlist = getvideos(subreddits, int(limit))
		template = loader.get_template('vidlist/player.html')
		context = RequestContext(request, {
			'playlist': playlist,
		})
		return HttpResponse(template.render(context))
	print "request POST"
	response_dict = {}
	subreddit = request.POST['subreddit'].split('/')[2]
	limit = request.POST['limit']
	subreddits.append(subreddit)
	playlist = getvideos(subreddits, int(limit))
	#Convert into
	for song in playlist:
		response_dict[song.videoid] = {'title' : song.title, 'source' : song.source, 'url' : song.url}

	response_json = simplejson.dumps(response_dict)
	template = loader.get_template('vidlist/playlist.html')
	context = RequestContext(request, {'songs' : playlist})
#	return TemplateResponse(request, template, {'songs' : playlist})
	return HttpResponse(template.render(context))
