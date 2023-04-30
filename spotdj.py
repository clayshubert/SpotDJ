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
    playlists = sp.current_user_playlists()

    return render_template("index.html", playlists=playlists)

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