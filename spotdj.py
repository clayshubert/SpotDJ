import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import numpy as np

from flask import Flask, render_template, request

from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/home")
def home():
    # authenticate with Spotify API
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    #Pull user data
    #user_name = user["display_name"]
    #user_image = user["images"][0]["url"]

    return render_template("home.html")

@app.route("/songoftheweek")
def get_song_of_the_week():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=["user-library-read", "user-top-read", "playlist-read-private", "user-read-playback-state", "user-modify-playback-state"]
    ))
    # Fetch top played tracks from the user's library
    top_tracks = sp.current_user_top_tracks(limit=25)['items']
    
    # Fetch tracks from user's playlists
    playlists = sp.current_user_playlists(limit=25)['items']
    playlist_tracks = []
    for playlist in playlists:
        tracks = sp.playlist_tracks(playlist['id'])['items']
        playlist_tracks.extend([track['track'] for track in tracks])
    
    # Combine top tracks and playlist tracks
    all_tracks = top_tracks + playlist_tracks
    
    # Get audio features to determine mood
    track_ids = [track['id'] for track in all_tracks]
    audio_features = sp.audio_features(track_ids)
    
    # Filter tracks based on mood (e.g., valence > 0.5 for positive mood)
    positive_mood_tracks = [track for track, feature in zip(all_tracks, audio_features) if feature['valence'] > 0.5]
    
    # Randomly select a song
    song_of_the_week = random.choice(positive_mood_tracks)
    
    return song_of_the_week['name'], song_of_the_week['artists'][0]['name']
     
@app.route("/shuffle", methods=["POST"])
def shuffle():
    # authenticate with Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=["user-library-read", "playlist-read-private", "user-read-playback-state", "user-modify-playback-state"]
    ))

    # get selected playlist id
    playlist_id = request.form["playlist_id"]

    # get tracks from the selected playlist
    tracks = sp.playlist_tracks(playlist_id)

    # shuffle tracks
    random.shuffle(tracks["items"])

    # create list of track uris
    uris = [track["track"]["uri"] for track in tracks["items"]]

    # play shuffled tracks
    # get available devices
    devices = sp.devices()

    # check if a device was selected in the form
    device_name = request.form.get("device_name")
    if device_name:
        # find the device ID of the selected device
        device_id = None
        for device in devices["devices"]:
            if device["name"] == device_name:
                device_id = device["id"]
                break

        # play shuffled tracks on the selected device
        if device_id:
            sp.start_playback(device_id=device_id, uris=uris)
            current_track = sp.current_playback()["item"]
        else:
            return "Device not found"
    else:
        # render the template with the list of available devices
        return render_template("shuffle.html", devices=[device["name"] for device in devices["devices"]], playlists=sp.current_user_playlists())

if __name__ == "__main__":
    app.run(debug=True)