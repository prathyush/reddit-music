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

"""
class Song:
	def __init__:
"""

def getJSON(subreddit, limit):
	url = "http://www.reddit.com/r/"+subreddit+"/.json?limit="+str(limit)
	print url
	f = urllib.urlopen(url)
	return json.load(f)

def getvideos(subreddits, limit):
	for subreddit in subreddits:
		try:
			json_data = getJSON(subreddit, limit)
			urlfeed = []
			title = []
			videos = []
			for i in json_data["data"]["children"]:
				if json.dumps(i["data"]["domain"]) in ('"youtube.com"'):
					urlfeed.append(json.dumps(i["data"]["url"]))
					title.append(json.dumps(i["data"]["title"]))
					url_data = urlparse.urlparse(json.dumps(i["data"]["url"])[1:-1])
					query = urlparse.parse_qs(url_data.query)
					video = query["v"][0]
					videos.append(video)

		except KeyError, e:
			print "Error: Malformed JSON return file"
		print urlfeed
		print title
		#for t in title:
		#		print t
		return videos

if __name__ == '__main__':
	subreddits = ['progmetal']
	getvideos(subreddits, 20)	
