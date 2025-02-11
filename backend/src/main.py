import os
from example_func import OutlierExample
from data_collect import get_data, process_data_from_db
from youtube_func import GoogleAPIFacade
from spotify_func import SpotifyAPIFacade
from flask import Flask, render_template, request, jsonify
import logging
import pandas
from requests import post
import json
import matplotlib.pyplot as plt
import pandas as pd
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<home>')
def name():
    return 'You typed home in the funny thing <home>'

def main():
    #OutlierExample()
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
    tracks = spotify_api.get_artist_album_tracks(
        spotify_api.name_to_id_adapter("artist","eminem"))
    
    print(json.dumps(tracks, indent=4))
    #logging.root.setLevel(logging.NOTSET)
    #logging.info("Starting Python FLask")
    #app.run(debug=True)

if __name__ == '__main__':
    main()