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
	def __init__ (self, videoid, title, url, source):
		self.videoid = videoid
		self.title = title
		self.url = url
		self.thumbnail_url = "http://i1.ytimg.com/vi/%s/hqdefault.jpg" % videoid
		self.source = source

def getRedditJSON(subreddit, limit):
	url = "http://www.reddit.com/r/"+subreddit+"/.json?limit="+str(limit)
	print url
	f = urllib.urlopen(url)
	return json.load(f)

def getvideos(subreddits, limit):
	for subreddit in subreddits:
		try:
			json_data = getRedditJSON(subreddit, limit)
			songs = []
			for i in json_data["data"]["children"]:
				domain = json.dumps(i["data"]["domain"])[1:-1]
				url = json.dumps(i["data"]["url"])[1:-1]
				url_data = urlparse.urlparse(url)
				query = urlparse.parse_qs(url_data.query)
				
				if domain == 'youtube.com':
					videoid = query["v"][0]
				elif domain in ('youtu.be', 'vimeo.com', 'soundcloud.com'):
					videoid = url_data.path[1:]
# Turned out expensive.
#					yt_url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % videoid
#					yt_json = json.load(urllib.urlopen(yt_url))
#					title = yt_json['entry']['title']['$t']
					title = str(json.dumps(i["data"]["title"])[1:-1])
					source = 'youtube.com' if domain == 'youtu.be' else domain
					print videoid, source, title, url
					songs.append(Song(videoid,title,url,source))

		except KeyError, e:
			print "Error: Malformed JSON return file"
		return songs

if __name__ == '__main__':
	subreddits = ['progmetal']
	songs_dict = {}
	songs = getvideos(subreddits, 50)
	for song in songs:
		songs_dict[song.videoid] = {'title' : song.title, 'source' : song.source, 'url' : song.url}
	print json.dumps(songs_dict)
