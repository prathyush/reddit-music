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


domains = ['youtu.be', 'youtube.com', 'soundcloud.com']

subreddits = ['/r/composer','/r/baroque','/r/classicalmusic','/r/contemporary','/r/concertband','/r/choralmusic','/r/ChamberMusic','/r/EarlyMusic','/r/earlymusicalnotation','/r/ElitistClassical','/r/icm','/r/Opera','/r/orchestra','/r/acidhouse','/r/ambientmusic','/r/AStateOfTrance','/r/AtmosphericDnB','/r/BigBeat','/r/boogiemusic','/r/breakbeat','/r/breakcore','/r/brostep','/r/chicagohouse','/r/chillout','/r/Chipbreak','/r/Chiptunes','/r/complextro','/r/darkstep','/r/DnB','/r/DubStep','/r/electronicdancemusic','/r/ElectronicJazz','/r/ElectronicBlues','/r/electrohiphop','/r/electrohouse','/r/electronicmagic','/r/ElectronicMusic','/r/electropop','/r/electroswing','/r/ExperimentalMusic','/r/fidget','/r/filth','/r/frenchelectro','/r/frenchhouse','/r/funkhouse','/r/fusiondancemusic','/r/futurebeats','/r/FutureFunkAirlines','/r/FutureGarage','/r/futuresynth','/r/gabber','/r/glitch','/r/glitchop','/r/Grime','/r/happyhardcore','/r/hardhouse','/r/hardstyle','/r/house','/r/idm','/r/industrialmusic','/r/ItaloDisco','/r/LiquidDubstep','/r/mashups','/r/minimal','/r/mixes','/r/moombahcore','/r/nightstep','/r/OldskoolRave','/r/partymusic','/r/psybient','/r/PsyBreaks','/r/psytrance','/r/purplemusic','/r/raggajungle','/r/RealDubstep','/r/skweee','/r/swinghouse','/r/tech_house','/r/Techno','/r/Trance','/r/tranceandbass','/r/trap','/r/tribalbeats','/r/ukfunky','/r/80sHardcorePunk','/r/90sAlternative','/r/90sRock','/r/AlternativeRock','/r/AltCountry','/r/AORMelodic','/r/ausmetal','/r/BlackMetal','/r/bluegrass','/r/Blues','/r/bluesrock','/r/CanadianClassicRock','/r/CanadianMusic','/r/ClassicRock','/r/country','/r/Christcore','/r/crunkcore','/r/deathcore','/r/deathmetal','/r/Djent','/r/DoomMetal','/r/Drone','/r/EmoScreamo','/r/flocked','/r/folk','/r/folkmetal','/r/folkpunk','/r/folkrock','/r/GaragePunk','/r/GothicMetal','/r/Grunge','/r/hardcore','/r/HardRock','/r/horrorpunk','/r/indie_rock','/r/jrock','/r/krautrock','/r/LadiesofMetal','/r/MathRock','/r/melodicdeathmetal','/r/MelodicMetal','/r/MetalNews','/r/Metalmusic','/r/metal','/r/metalcore','/r/monsterfuzz','/r/neopsychedelia','/r/NewWave','/r/noiserock','/r/numetal','/r/pianorock','/r/poppunkers','/r/PostHardcore','/r/PostRock','/r/powermetal','/r/powerpop','/r/ProgMetal','/r/progrockmusic','/r/PsychedelicRock','/r/punk','/r/Punkskahardcore','/r/Punk_Rock','/r/Rock','/r/shoegaze','/r/stonerrock','/r/symphonicblackmetal','/r/symphonicmetal','/r/synthrock','/r/truethrash','/r/Truemetal','/r/OutlawCountry','/r/WomenRock','/r/90sHipHop','/r/altrap','/r/asianrap','/r/backspin','/r/ChapHop','/r/Gfunk','/r/HipHopHeads','/r/Rap','/r/rapverses','/r/trapmuzik','/r/2010smusic','/r/2000smusic','/r/90sMusic','/r/80sMusic','/r/70sMusic','/r/60sMusic','/r/50sMusic','/r/70s','/r/Acappella','/r/AcousticCovers','/r/afrobeat','/r/animemusic','/r/balkanbrass','/r/balkanmusic','/r/boomswing','/r/bossanova','/r/britpop','/r/carmusic','/r/concerts','/r/chillmusic','/r/cpop','/r/CrappyMusic','/r/dembow','/r/disco','/r/DreamPop','/r/Elephant6','/r/Exotica','/r/FilmMusic','/r/FunkSouMusic','/r/gamemusic','/r/GypsyJazz','/r/HispanicMusic','/r/IndieFolk','/r/Irishmusic','/r/ItalianMusic','/r/jambands','/r/jazz','/r/jpop','/r/kpop','/r/listentoconcerts','/r/klezmer','/r/lt10k','/r/MelancholyMusic','/r/minimalism_music','/r/motown','/r/MovieMusic','/r/muzyka','/r/oldiemusic','/r/OldiesMusic','/r/pianocovers','/r/PopMusic','/r/PoptoRock','/r/rainymood','/r/recordstorefinds','/r/reggae','/r/remixxd','/r/RetroMusic','/r/rnb','/r/rootsmusic','/r/SalsaMusic','/r/Ska','/r/songbooks','/r/Soulies','/r/SoundsVintage','/r/SpaceMusic','/r/swing','/r/Tango','/r/TheRealBookVideos','/r/TouhouMusic','/r/TraditionalMusic','/r/treemusic','/r/triphop','/r/VintageObscura','/r/vocaloid','/r/WorldMusic','/r/audioinsurrection','/r/danktunes','/r/albumaday','/r/albumoftheday','/r/Albums','/r/albumlisteners','/r/bassheavy','/r/Catchysongs','/r/Chopping','/r/CircleMusic','/r/CoverSongs','/r/DANCEPARTY','/r/EarlyMusic','/r/earlymusicalnotation','/r/FemaleVocalists','/r/findaband','/r/freemusic','/r/Frisson','/r/gameofbands','/r/GayMusic','/r/germusic','/r/gethightothis','/r/FitTunes','/r/HeadNodders','/r/heady','/r/HeyThatWasIn','/r/HighFidelity','/r/ifyoulikeblank','/r/indie','/r/IndieWok','/r/Instrumentals','/r/ipm','/r/IsolatedVocals','/r/LetsTalkMusic','/r/listentoconcerts','/r/listentomusic','/r/listentonews','/r/ListenToThis','/r/ListenToUs','/r/livemusic','/r/llawenyddhebddiwedd','/r/Lyrics','/r/mainstreammusic','/r/MiddleEasternMusic','/r/MLPtunes','/r/Music','/r/MusicAlbums','/r/musicsuggestions','/r/MusicToSleepTo','/r/musicvideos','/r/NewAlbums','/r/newmusic','/r/onealbumaweek','/r/partymusic','/r/RedditOriginals','/r/RepublicOfMusic','/r/RoyaltyFreeMusic','/r/runningmusic','/r/Samples','/r/SpotifyMusic','/r/ThemVoices','/r/unheardof','/r/WTFMusicVideos','/r/AlbumArtPorn','/r/albumreviews','/r/Audio','/r/Audiophile','/r/AustinMusicians','/r/bandmembers','/r/CarAV','/r/CassetteCulture','/r/Cd_collectors','/r/ConcertTickets','/r/germusic','/r/ICoveredASong','/r/ifyoulikeblank','/r/independentmusic','/r/ineedasong/','/r/japanesemusic','/r/koreanmusic','/r/LubbockMusicians','/r/mixcd','/r/musiccritics','/r/musicessentials','/r/MusicEventMeetUp','/r/musicfestivals','/r/musicnews','/r/MusiciansBlogs','/r/Musicians','/r/OSOM','/r/performer','/r/RecordClub','/r/recordstore','/r/redditmusicclub','/r/Rockband','/r/RockbandChallenges','/r/TipOfMyTongue','/r/TouringMusicians','/r/vinyl','/r/VinylReleases','/r/WeAreTheMusicMakers','/r/AcousticOriginals','/r/Composer','/r/ICoveredASong','/r/MusicCritique','/r/MusicInTheMaking','/r/MyMusic','/r/RadioReddit','/r/ratemyband','/r/Songwriters','/r/TheseAreOurAlbums','/r/ThisIsOurMusic','/r/independentmusic','/r/300Songs','/r/311','/r/ArcadeFire','/r/APerfectCircle','/r/TheAvettBrothers','/r/BaysideIsACult','/r/TheBeachBoys','/r/Beatles','/r/billytalent','/r/Blink182','/r/BMSR','/r/boniver','/r/brandnew','/r/BruceSpringsteen','/r/Burial','/r/cityandcolour','/r/Coldplay','/r/CutCopy','/r/TheCure','/r/DaftPunk','/r/DavidBowie','/r/Deadmau5','/r/DeepPurple','/r/Deftones','/r/DieAntwoord','/r/DMB','/r/elliegoulding','/r/empireofthesun','/r/EnterShikari','/r/feedme','/r/FirstAidKit','/r/flaminglips','/r/franzferdinand','/r/Gorillaz','/r/gratefuldead','/r/Greenday','/r/GunsNRoses','/r/Incubus','/r/JackWhite','/r/John_frusciante','/r/kings_of_leon','/r/ladygaga','/r/lanadelrey','/r/lennykravitz','/r/Led_Zeppelin','/r/Macklemore','/r/Manowar','/r/MattAndKim','/r/Megadeth','/r/Metallica','/r/MGMT','/r/MinusTheBear','/r/ModestMouse','/r/Morrissey','/r/MyChemicalRomance','/r/Muse','/r/NeilYoung','/r/NIN','/r/Nirvana','/r/oasis','/r/Opeth','/r/OFWGKTA','/r/OutKast','/r/panicatthedisco','/r/PearlJam','/r/phish','/r/Pinback','/r/PinkFloyd','/r/porcupinetree','/r/prettylights','/r/Puscifer','/r/Queen','/r/Radiohead','/r/RATM','/r/RedHotChiliPeppers','/r/The_Residents','/r/RiseAgainst','/r/Rush','/r/SigurRos','/r/slipknot','/r/TheKillers','/r/TheOffspring','/r/TheStrokes','/r/TheMagneticZeros','/r/UnicornsMusic','/r/Slayer','/r/SmashingPumpkins','/r/SparksFTW','/r/ToolBand','/r/tragicallyhip','/r/U2Band','/r/Umphreys','/r/velvetunderground','/r/Ween','/r/weezer','/r/WeirdAl','/r/yesband','/r/Zappa','/r/AlbumArtPorn','/r/BandPorn','/r/concertporn','/r/InstrumentPorn','/r/MetalMemes','/r/MusicPics','/r/GrooveSharkPlaylists','/r/DJs','/r/PirateRadio','/r/Spotify','/r/Turntablists','/r/abletonclass','/r/bandmembers','/r/bassLessons','/r/DancePerformance','/r/earlymusicalnotation','/r/Ethnomusicology','/r/ExplainThisSong','/r/GuitarLessons','/r/LearnMusic','/r/MusicEd','/r/musicindustry','/r/MusicInstructor','/r/musicology','/r/MusicTheory','/r/solresol','/r/tabs','/r/Accordion','/r/banjo','/r/Bass','/r/Bassoon','/r/beatbox','/r/brass','/r/Cello','/r/Clarinet','/r/ClassicalGuitar','/r/DoubleBass','/r/Drummers','/r/Drums','/r/Flute','/r/Guitar','/r/hammondorgan','/r/handpan','/r/harmonica','/r/Horn','/r/keys','/r/luthier','/r/Oboe','/r/Ocarina','/r/Percussion','/r/Percussionists','/r/Piano','/r/Piccolo','/r/Recorder','/r/saxophone','/r/saxophonics','/r/Singing','/r/synthesizers','/r/Telecaster','/r/Trombone','/r/Trumpet','/r/tuba','/r/ukulele','/r/viola','/r/Violinist','/r/AudioEngineering','/r/EDMproduction','/r/FL_Studio','/r/AbletonLive','/r/AudioPost','/r/Cubase','/r/futurebeatproducers','/r/GameAudio','/r/linuxaudio','/r/LocationSound','/r/Logic_Studio','/r/MaxMSP','/r/ProductionLounge','/r/Protools','/r/RateMyAudio','/r/Reaper','/r/Reasoners','/r/Remix','/r/Renoise','/r/Samplehunters','/r/SongStems','/r/VSTi','/r/DIYGear','/r/Gear4Sale','/r/GuitarPedals','/r/skullcandy','/r/Synthesizers']

class Song:
	def __init__ (self, videoid, title, url, source):
		self.videoid = videoid
		self.title = title
		self.url = url
		self.thumbnail_url = "http://i1.ytimg.com/vi/%s/hqdefault.jpg" % videoid
		self.source = source
	def to_json(self):
		return {'videoid': self.videoid, 'title' : self.title, 'url' : self.url, 'thumbnail_url' : self.thumbnail_url, 'source' : self.source}

def getRedditJSON(subreddit, limit):
	url = "http://www.reddit.com/r/"+subreddit+"/.json?limit="+str(limit)
	print url
	f = urllib.urlopen(url)
	return json.load(f)

retries = 0;
def getvideos(subreddits, limit):
	global retries;
	for subreddit in subreddits:
		try:
			json_data = getRedditJSON(subreddit, limit)
			songs = []
			for i in json_data["data"]["children"]:
				domain = json.dumps(i["data"]["domain"])[1:-1]

				if domain not in domains:
					continue;
				url = json.dumps(i["data"]["url"])[1:-1]
				url_data = urlparse.urlparse(url)
				query = urlparse.parse_qs(url_data.query)
				title = str(json.dumps(i["data"]["title"])[1:-1])
				videoid = query["v"][0] if domain == 'youtube.com' else url_data.path[1:]
				source = 'youtube.com' if domain == 'youtu.be' else domain
				print videoid, source, title, url
				songs.append(Song(videoid,title,url,source))

		except KeyError, e:
			print "Error: Malformed JSON return file"
			time.sleep(2);

			if retries < 3:
				retries += 1;
				return getvideos(subreddits, limit);
			else:
				retries = 0;
				return None

		return songs
def getSubreddits():
	return subreddits

if __name__ == '__main__':
	subreddits = ['progmetal']
	songs_dict = {}
	songs = getvideos(subreddits, 50)
	for song in songs:
		songs_dict[song.videoid] = {'title' : song.title, 'source' : song.source, 'url' : song.url}
	print json.dumps(songs_dict)
