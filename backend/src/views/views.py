from flask import Blueprint, Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from forms import *
import base64
from io import BytesIO
from spotify_func import *
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from mongo_func import *
from scipy.interpolate import interp1d 
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import os 
import csv

# NOTE: 
# 1. I am using a local csv file since, the mongodb is missing famous artist,
# which makes testing a pain to do
# 2. This was programmed horribly since I was ina rush. If I had more time I would
#   a. Rewrite the logic to dynamically produce the figures and tables (using a for loop)
#   b. Rewrite the inputs as list instead of discrete variables

NUMBER_OF_ELEMENTS = 4
spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
mongodb_api = MongoDBFacade("MONGO_CONNECTION_STRING")
artist_info_csv = pd.read_csv("temp/CLEANED_featured_Spotify_artist_info.csv")


views = Blueprint("views", __name__)    
@views.route('/')
def index():
    return render_template('index.html')
@views.route('/album', methods=['GET', 'POST'])
def album():
    print("Loading album page:")
    album,  album_1, album_2, album_3, form = read_input(InputForm)
    if album:
        pass
    return render_template('album.html', input = album, form = form)

@views.route('/artist', methods=['GET','POST'])
def artist():
    print("Loading artist page Dir: ", os.getcwd())
    artist, artist_1, artist_2, artist_3, form = read_input(InputForm)
    artist_data = None
    artist_image = None
    artist_top_tracks = []
    histogram_html = None
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
        artist_top_tracks.append(spotify_api.get_artist_top_tracks(ids.iloc[0]))
        #histogram_html = artist_popularity_history(artist_top_tracks)
        # TODO: Write a fail safe for when we cannot find the artist


    return render_template('artist.html', 
                            input = artist,
                            form = form, 
                            output = artist_data,
                            image_url = artist_image,
                            histogram = histogram_html)

@views.route('/genre', methods=['GET', 'POST'])
def genre(): 
    print("Loading genre page")
    histogram_html = None
    comparisons = []
    genre_match = [] # Genres that exist on the spotify platform
    recommendations = []
    genres = [None] * NUMBER_OF_ELEMENTS # Genres the user entered to the website
    genres[0], genres[1], genres[2], genres[3], form = read_input(InputForm)
    genre_data = None
    timeline_html = None
    
    print(f"Genre 1: {genres[0]}, Genre 2: {genres[1]}, Genre 3: {genres[2]}, Genre 4: {genres[3]}")

    move_empty_elements_back(genres)

    if genres[0]:
        for genre in genres:
            if not genre:
                break
            
            filtered_df = artist_info_csv[
                artist_info_csv["genres"].str.contains(
                    genre.lower(), case=False, na=False)].copy()
            
            recommendations.append(apriori_algorithm(genre)) 
            if not filtered_df.empty:
                filtered_df["Genre"] = genre 
                genre_match.append(genre)
                comparisons.append(filtered_df)
            
        if comparisons: # Checks if any genre the user entered exist in the database
            df_combined = pd.concat(comparisons)

            fig = px.histogram(df_combined, x="popularity", color="Genre", 
                               barmode="overlay", nbins=100,
                               title="Popularity Distribution of the Genres")
            
            fig.update_layout(xaxis_title="Popularity",
                            yaxis_title="Count", bargap=0.2)
            
            histogram_html = fig.to_html(full_html=False)
            timeline_html = create_genre_popularity_history_plot(genre_match)
        print(recommendations[0])

    return render_template('genre.html', inputs=genres,
                           form=form, output=genre_data, 
                           histogram=histogram_html, 
                           suggestions=recommendations, 
                           timeline = timeline_html)

@views.route('/track', methods=['GET', 'POST'])
def track():
    print("Loading track page")
    track, track_1, track_2, track_3,  form = read_input(InputForm)
    if track:

        df = pd.read_csv("backend/tracks.csv")
        tracks = df[df["genres"].str.contains(genre.lower(), case=False, na=False)]
        pass
    return render_template('track.html', input = track, form = form)

@views.route('/about')
def about():
    print("Loading about page")
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

# VERY SLOW, NEEDS A WHOLE REWRITE!!!! - Jonathan Duggan 2024-03-24

def apriori_algorithm(genre):
    genre = genre.lower()
    
    mask = artist_info_csv["genres"].str.contains(genre, case=False, na=False)
    filtered_df = artist_info_csv.loc[mask, "genres"]

    items = [x.split(', ') for x in filtered_df if isinstance(x, str)]

    encoder = TransactionEncoder()
    encoded_items = encoder.fit_transform(items)
    
    df_sample = pd.DataFrame(encoded_items, columns=encoder.columns_, dtype=bool)

    print(f'Number of transactions: {df_sample.shape[0]}')
    print(f'Number of unique items: {df_sample.shape[1]}')

    support_count = len(df_sample) / 1000
    df_itemset_max_1 = apriori(df_sample, min_support=support_count / len(df_sample), use_colnames=True)

    df_itemset_max_1["itemsets"] = df_itemset_max_1["itemsets"].apply(lambda x: ', '.join(x))

    print("Results: ", df_itemset_max_1.head(25))
    
    return df_itemset_max_1.head(20).tail(15).to_dict(index=True, orient="records")

# Find a better data set PLEASE! the one on mongodb DOES NOT HAVE RAP
# also, k-pop crashes the server, probably because of the - token maybe? 
# Just go on kraggle and look for one brother 
# - Jonathan Duggan 2025-03-26
def create_genre_popularity_history_plot(genres):
    genre_history = mongodb_api.client["music"]
    print("genre popularity history", genres)
    result = genre_history["genre_history"].aggregate([
    {
        "$match": {
          "name": {"$in": genres },
          "count": {"$gte": 2},
        }
    }
    ])

    df = pd.DataFrame(result)
    fig = go.Figure()
    df["release_date"] = pd.to_datetime(df["release_date"], format="%Y")
    print("Unique Genres in Data:", df["name"].unique())
    print(df)
    for genre in genres:
        df_genre = df[df["name"] == genre].sort_values(by="release_date")

        if df_genre.empty:
            continue 

        x = df_genre["release_date"]
        y = df_genre["popularity"]

        n = np.arange(len(x))

        # Replace interpld function, it's deprecated 
        x_spline = interp1d(n, x.astype(np.int64), kind="linear")
        y_spline = interp1d(n, y, kind="cubic")

        
        n_ = np.linspace(n.min(), n.max(), 500)
        x_ = pd.to_datetime(x_spline(n_))
        y_ = y_spline(n_)

        
        fig.add_trace(go.Scatter(x=x_, y=y_, mode="lines", name=genre))

    fig.update_layout(
        title="Popularity Over Time for Multiple Genres",
        xaxis_title="Release Date",
        yaxis_title="Popularity",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
    )

    return fig.to_html(full_html=False)

def artist_popularity_history(artist_ids):
    for artist_id in artist_ids:
        spotify_api.get_artist_album_tracks()
    spotify_api.get_artist_album_tracks() 
    comparisons = []
    for tracks in artists_top_tracks: 
        track_names_and_pop = list(map(lambda x: {
            #"release_date" : x["album"]["release_date"],
            "name" : x["name"],
            "popularity": x["popularity"]},
            tracks['tracks']
        ))
        track_df = pd.DataFrame(track_names_and_pop)
        comparisons.append(track_df)
    
    df_combined = pd.concat(comparisons)
    
    fig = px.histogram(df_combined, x="popularity", color="name", 
                        barmode="overlay", nbins=100,
                        title="Popularity Distribution of the Artists Tracks")
    
    fig.update_layout(xaxis_title="Popularity",
                      yaxis_title="Count", bargap=0.2)
            
    return fig.to_html(full_html=False)