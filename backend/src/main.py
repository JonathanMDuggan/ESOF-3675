import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import logging
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<home>')
def name():
    return 'You typed home in the funny thing <home>'

#def print_saved_tracks():
#    scope = "user-library-read"     
#    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))   
#    results = sp.current_user_saved_tracks()
#    for i, item in enumerate(result['items']):
#        track = item['track']
#        print(i, track['artists'][0]['name'], " - " track['name'])
#

# Load the api from the .env file
def load_api(API_CLIENT_ID_NAME: str, API_CLIENT_SECERT_NAME: str):
    CLIENT_ID     = os.getenv(API_CLIENT_ID_NAME)
    CLIENT_SECERT = os.getenv(API_CLIENT_SECERT_NAME)
    if CLIENT_ID == None or CLIENT_SECERT == None:
        logging.error("%s is: %s", API_CLIENT_ID_NAME, CLIENT_ID)
        logging.error("%s is: %s", API_CLIENT_SECERT_NAME, CLIENT_SECERT)
    else:
        logging.info("Successfully loaded %s and %s", API_CLIENT_ID_NAME, API_CLIENT_SECERT_NAME)
    return CLIENT_ID, CLIENT_SECERT
    

def main():
    # Set the logging level to its lowest level
    logging.root.setLevel(logging.NOTSET)
    logging.info("Starting Python FLask")
    # load the spotify api
    load_dotenv()
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECERT = load_api("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECERT")
    app.run(debug=True)

if __name__ == '__main__':
    main()