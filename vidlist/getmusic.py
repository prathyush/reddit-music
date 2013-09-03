#!/usr/bin/python

#
# Extract youtube links from Music subreddits.
#

import os
import sys
import time
from urllib2 import Request, urlopen, URLError, HTTPError
import urllib
import json
from pprint import pprint
import urlparse

class Song:
	def __init__ (self, videoid, title, url):
		self.videoid = videoid
		self.title = title
		self.url = url
		self.thumbnail_url = "http://i1.ytimg.com/vi/%s/hqdefault.jpg" % videoid

def getJSON(subreddit, limit):
	url = "http://www.reddit.com/r/"+subreddit+"/.json?limit="+str(limit)
	print url
	f = urllib.urlopen(url)
	return json.load(f)

def getvideos(subreddits, limit):
	for subreddit in subreddits:
		try:
			json_data = getJSON(subreddit, limit)
			songs = []
			for i in json_data["data"]["children"]:
				if json.dumps(i["data"]["domain"]) in ('"youtube.com"'):
					url = json.dumps(i["data"]["url"])
#					title = str(json.dumps(i["data"]["title"])[1:-1])
					url_data = urlparse.urlparse(json.dumps(i["data"]["url"])[1:-1])
					query = urlparse.parse_qs(url_data.query)
					videoid = query["v"][0]
					yt_url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % videoid 
					yt_json = json.load(urllib.urlopen(yt_url))
					title = yt_json['entry']['title']['$t']
					songs.append(Song(videoid,title,url))

		except KeyError, e:
			print "Error: Malformed JSON return file"
		return songs

if __name__ == '__main__':
	subreddits = ['progmetal']
	getvideos(subreddits, 20)
