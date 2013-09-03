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
					title = json.dumps(i["data"]["title"])
					url_data = urlparse.urlparse(json.dumps(i["data"]["url"])[1:-1])
					query = urlparse.parse_qs(url_data.query)
					video = query["v"][0]
					songs.append(Song(video,title,url))

		except KeyError, e:
			print "Error: Malformed JSON return file"
		return songs

if __name__ == '__main__':
	subreddits = ['progmetal']
	getvideos(subreddits, 20)
