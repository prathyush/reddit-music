# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from getmusic import getvideos, Song

def index(request):
	subreddits = []
	subreddit = request.GET.get('s','progmetal')
	subreddits.append(subreddit)
	playlist = getvideos(subreddits, 200)
	template = loader.get_template('vidlist/index.html')
	context = RequestContext(request, {
		'playlist': playlist,
	})
	return HttpResponse(template.render(context))
