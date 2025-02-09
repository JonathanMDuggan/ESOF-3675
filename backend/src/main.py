import os
from youtube_func import GoogleAPIFacade
from spotify_func import SpotifyAPIFacade
from flask import Flask, render_template, request, jsonify
import logging
from requests import post
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<home>')
def name():
    return 'You typed home in the funny thing <home>'

def main():
    # Set the logging level to its lowest level
    google_api = GoogleAPIFacade("YOUTUBE_API_KEY")
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
    spotify_api.search_for_item("track", "Beat it")
    youtube = google_api.get_youtube()
    request = youtube.channels().list(
        part='statistics',
        forUsername='sentdex'
    )

    response = request.execute()
    print(response)
    #spotify_api.search_for_item("artist","eminem", 5)
    logging.root.setLevel(logging.NOTSET)
    logging.info("Starting Python FLask")
    # load the spotify api
    app.run(debug=True)

if __name__ == '__main__':
    main()