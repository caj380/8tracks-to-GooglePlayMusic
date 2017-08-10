import os
import cgi
import json
import time
import pickle
import string
import urllib
import gmusicapi
import unicodedata
import urllib, urllib2
from xml.etree.ElementTree import *

google_username = "YOUR_GOOGLE_EMAIL_ADDERSS"
google_password = "YOUR_GOOGLE_PASSWORD"
eighttracks_username = "YOUR_8TRACKS_USERNAME"

playlist_id = "YOUR_PLAYLIST_ID" # Try running "python get-playlist-ids.py 'YOUR_GOOGLE_EMAIL_ADDERSS' 'YOUR_GOOGLE_PASSWORD'" to find your playlist IDs

# Log in.
api = gmusicapi.Mobileclient()
if not api.login(google_username, google_password, gmusicapi.Mobileclient.FROM_MAC_ADDRESS):
	print "Login error"

def fetch_songs(username):
	consol = []

	for pagenum in range(0, 1): #99
		url = "http://8tracks.com/users/" + username + "/favorite_tracks?page=" + str(pagenum) + "&per_page=20&format=jsonh"

		headers = { 'User-Agent' : 'Mozilla/5.0' }
		req = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req)

		gotten = response.read()

		consol.append(gotten)

		if gotten.find('"next_page":null') > -1:
			break

	try:
		k = json.JSONDecoder().decode(consol[0])
	except:
		print 'something went wrong :('
		
		return

	if k['status'] == "404 Not Found":
		print 'Invalid username :('
		
		return

	tracklist = []

	trackcount = 1


	for xml in range(0, len(consol)):
		k = json.JSONDecoder().decode(consol[xml])
		for tk in range(0, len(k["favorite_tracks"])):
			track = k["favorite_tracks"][tk]['name']
			artist = k["favorite_tracks"][tk]['performer']
			tracklist.append((artist,track))

			#print track
			trackcount += 1
	#print tracklist
	return tracklist
	
def add_songs(starred):
	print playlist_id

	to_add = []
	
	for target in starred:
		try:
			res = api.search(target[0] + " " + target[1], max_results=1)
			to_add.append('T' + res["song_hits"][0]["track"]["nid"])
		except:
			pass
		print "Got " + str(len(to_add)) + " songs so far out of " + str(len(starred))
	
	to_add.reverse()
	print "Adding " + str(len(to_add)) + " songs to playlist"

	print to_add
	added = api.add_songs_to_playlist(playlist_id, to_add)
	print added

	print "Successfully added " + str(len(added)) + " songs to playlist"
	
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def checkforsongs(runcount):
	if runcount == 1:
		try:
			with open ('songs.txt', 'rb') as fp:
				songs = pickle.load(fp)
		except:
			songs = []
			with open('songs.txt', 'wb') as fp:
				pickle.dump(songs, fp)
	else:
		songs = fetch_songs(eighttracks_username)
	while (songs==fetch_songs(eighttracks_username)):
		print "No new Songs."
		time.sleep(300) #20
	newsongs = fetch_songs(eighttracks_username)
	with open('songs.txt', 'wb') as fp:
		pickle.dump(newsongs, fp)
	newsongs2 = []
	for i in newsongs:
		if i not in songs:
			newsongs2.append(i)
	newsongs2 = remove_duplicates(newsongs2)
	print newsongs2
	return newsongs2

runcount = 1
while True:
		songs = checkforsongs(runcount)
		runcount += 1
		add_songs(songs)