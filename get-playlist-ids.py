import sys
import gmusicapi

google_username = sys.argv[1]
google_password = sys.argv[2]

# Log in.
api = gmusicapi.Mobileclient()
if not api.login(google_username, google_password, gmusicapi.Mobileclient.FROM_MAC_ADDRESS):
	print "Login error"

playlists = api.get_all_playlists()

for playlist in playlists:
	print "Name: " + playlist['name']
	print "Playlist id: " + playlist['id'] + "\n"