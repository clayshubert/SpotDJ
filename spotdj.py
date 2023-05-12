import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
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
    # authenticate with Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=["user-library-read", "playlist-read-private"]))

    # get user's playlists
    #playlists = sp.current_user_playlists()

    return render_template("home.html")

@app.route("/shuffle", methods=["GET", "POST"])
def shuffle():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=["user-library-read", "playlist-read-private", "user-read-playback-state", "user-modify-playback-state"]
        ))
    devices = sp.devices()

    if request.method == 'POST':
        playlist_id = request.form['playlist_id']
        # get tracks from the selected playlist
        tracks = sp.playlist_tracks(playlist_id)
        # shuffle tracks
        random.shuffle(tracks["items"])
  
        # create list of track uris
        uris = [track["track"]["uri"] for track in tracks["items"]]

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
        return render_template('shuffle.html', playlists=sp.current_user_playlists(), shuffled_tracks=uris)
    else:
        return render_template('shuffle.html', playlists=sp.current_user_playlists(), devices=[device["name"] for device in devices["devices"]])

@app.route("/smartmix", methods=["GET", "POST"])
def smartmix():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=["user-library-read", "playlist-read-private", "user-read-playback-state", "user-modify-playback-state"]
        ))
    devices = sp.devices()

    if request.method == "POST":
        # Get selected playlist ID from form data
        playlist_id = request.form["playlist_id"]

        # Get track IDs and audio features for the playlist
        tracks = sp.playlist_tracks(playlist_id)
        # create list of track uris
        uris = [track["track"]["uri"] for track in tracks["items"]]
        #audio_features = sp.audio_features(uris)

        # Use AI to shuffle tracks based on audio features
        # shuffle the playlist based on audio features
        shuffled_uris = []
        for i, track_uri in enumerate(uris):
            # get the audio features for the current track
            track_features = sp.audio_features(track_uri)[0]
            # find similar tracks based on audio features
            similar_uris = []
            for j, track_uri2 in enumerate(uris):
                track2_features = sp.audio_features(track_uri2)[0]
                if i != j and track_features != None and track2_features != None:
                    similarity = abs(track_features['danceability'] - track2_features['danceability']) + \
                                 abs(track_features['tempo'] - track2_features['tempo']) + \
                                 abs(track_features['energy'] - track2_features['energy'])
                    if similarity < 0.5:
                        similar_uris.append(uris[j])
            # shuffle the list of similar tracks and select the first 5
            random.shuffle(similar_uris)
            selected_uris = similar_uris[:5]
            # add the current track and the selected similar tracks to the shuffled list
            shuffled_uris.append(track_uri)
            shuffled_uris.extend(selected_uris)


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
            sp.start_playback(device_id=device_id, uris=shuffled_uris)
            #current_track = sp.current_playback()["item"]
        else:
            return "Device not found"
        return render_template('smartmix.html', playlists=sp.current_user_playlists(), shuffled_tracks=shuffled_uris)
    else:
        return render_template('smartmix.html', playlists=sp.current_user_playlists(), devices=[device["name"] for device in devices["devices"]])


@app.route("/aidj", methods=["POST"])
def aidj():

    return render_template("aidj.html")

if __name__ == "__main__":
    app.run(debug=True)