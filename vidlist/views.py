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
	response_dict = {}
	if not request.POST:
		subreddit = request.GET.get('s')
		template = loader.get_template('vidlist/player.html')
		if subreddit is not None:
			#Some one is messing around.
			print "Really? subreddit: "+subreddit
			limit = request.GET.get('l', '20')
			subreddits.append(subreddit)
			playlist = getvideos(subreddits, int(limit))
			#Convert into JSON. 
			for song in playlist:
				response_dict[song.videoid] = {'title' : song.title, 'source' : song.source, 'url' : song.url}
			response_json = simplejson.dumps(response_dict)
			context = RequestContext(request, {
				'playlist_json': response_json,
				'subreddit': subreddit,
				'playlist': playlist,
			})
		else:
			print "Usual Execution"
			context= RequestContext(request, {})
		return HttpResponse(template.render(context))

	subreddit = request.POST['subreddit'].split('/')[2]
	limit = request.POST['limit']
	subreddits.append(subreddit)
	playlist = getvideos(subreddits, int(limit))
	template = loader.get_template('vidlist/playlist.html')
	context = RequestContext(request, {'playlist' : playlist})
#	return TemplateResponse(request, template, {'songs' : playlist})
	return HttpResponse(template.render(context))
