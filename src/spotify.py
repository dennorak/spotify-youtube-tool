import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values
import json

class Playlist:
    def __init__(self, data):
        self.name = data["name"]
        self.songs =  data["tracks"]["items"]

    def getTrack(self, id):
        return self.songs[id]["track"]["name"] + " " + self.songs[id]["track"]["artists"][0]["name"]

    def count(self):
        return len(self.songs)

class Spotify:
    def __init__(self):
        config = dotenv_values()
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=config['CLIENT_ID'],
            client_secret=config['CLIENT_SECRET'],
            redirect_uri=config['REDIRECT_URL'],
            scope="user-library-read"
        ))
        
    def get_playlist(self, uri):
        return Playlist(self.sp.playlist(uri))

