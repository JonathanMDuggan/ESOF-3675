from flask import Blueprint, Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from forms import *
from spotify_func import *
import pandas as pd
from mongo_func import *
import os 
import csv
views = Blueprint("views", __name__)    
@views.route('/')
def index():
    return render_template('index.html')
@views.route('/album', methods=['GET', 'POST'])
def album():
    album,  album_1, album_2, album_3, form = read_input(InputForm)
    if album:
        pass
    return render_template('album.html', input = album, form = form)

@views.route('/artist', methods=['GET','POST'])
def artist():
    print("I LOVE MINECRAFT! Dir: ", os.getcwd())
    artist, artist_1, artist_2, artist_3, form = read_input(InputForm)
    artist_data = None
    artist_image = None
    if artist:
        spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
        mongodb_api = MongoDBFacade("MONGO_CONNECTION_STRING")

        # TODO: Add a search mongodb section before using the local computer
        # Look for artist name in the mongodb database
        # artist_database = mongodb_api.get_collection("music", "artist")

        # Not there?, Search the local data base
        df = pd.read_csv("temp/CLEANED_featured_Spotify_artist_info.csv")
        ids = df.loc[df["names"].str.lower() == artist.lower(), "ids"] 
        artist_data = spotify_api.get_artist(ids.iloc[0])
        artist_image = artist_data["images"][0]["url"] if "images" in artist_data and artist_data["images"] else None

        # TODO: Write a fail safe for when we cannot find the artist


    return render_template('artist.html', 
                            input = artist,
                            form = form, 
                            output = artist_data,
                            image_url = artist_image)

@views.route('/genre', methods=['GET', 'POST'])
def genre():
    genres = [None] * 4
    genres[0], genres[1], genres[2], genres[3], form = read_input(InputForm)
    tracks = None
    genre_data = None
    move_empty_elements_back(genres)
    if genres[0]:
        spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
        mongodb_api = MongoDBFacade("MONGO_CONNECTION_STRING")

        # TODO: Replace the local with the mongoDB Server 
        df = pd.read_csv("temp/CLEANED_featured_Spotify_artist_info.csv")
        tracks = df[df["genres"].str.contains(genres[0].lower(), case=False, na=False)]

        genre_data = tracks.to_html(classes="table table-striped", border=0)
    
    return render_template('genre.html', input = genres[0], form = form, output = genre_data, input_comparison_1 = genres[1])

@views.route('/track', methods=['GET', 'POST'])
def track():
    track, track_1, track_2, track_3,  form = read_input(InputForm)
    if track:
        spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
        mongodb_api = MongoDBFacade("MONGO_CONNECTION_STRING")

        df = pd.read_csv("backend/tracks.csv")
        tracks = df[df["genres"].str.contains(genre.lower(), case=False, na=False)]
        pass
    return render_template('track.html', input = track, form = form)

@views.route('/about')
def about():
    return render_template('about.html')

def read_input(form_class):
    input_value = None
    input_comparison_1 = None
    input_comparison_2 = None
    input_comparison_3 = None

    form = form_class()

    if form.validate_on_submit():
        input_value = form.input.data
        input_comparison_1 = form.input_comparison_1.data
        input_comparison_2 = form.input_comparison_2.data
        input_comparison_3 = form.input_comparison_3.data
        form.input.data = ''
        form.input_comparison_1.data = ''
        form.input_comparison_2.data = ''
        form.input_comparison_3.data = ''
        
    return input_value, input_comparison_1, input_comparison_2, input_comparison_3, form

def move_empty_elements_back(items):
    return sorted(items, key=lambda x: not bool(x))