# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
import getmusic

def index(request):
	playlist = getmusic.getvideos(['progmetal'], 60)
	template = loader.get_template('vidlist/index.html')
	context = RequestContext(request, {
		'playlist': playlist,
	})
	return HttpResponse(template.render(context))
