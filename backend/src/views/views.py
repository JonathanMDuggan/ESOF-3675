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
from mongo_func import *
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
    print("Loading genre page")
    fig_html = None
    comparisons = []
    recommendations = []
    genres = [None] * NUMBER_OF_ELEMENTS
    genres[0], genres[1], genres[2], genres[3], form = read_input(InputForm)
    genre_data = None
    
    print(f"Genre 1: {genres[0]}, Genre 2: {genres[1]}, Genre 3: {genres[2]}")

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
                comparisons.append(filtered_df)
            
        if comparisons:
            df_combined = pd.concat(comparisons)

            fig = px.histogram(df_combined, x="popularity", color="Genre", 
                               barmode="overlay", nbins=100,
                               title="Popularity Distribution of the Genres")
            
            fig.update_layout(xaxis_title="Popularity",
                            yaxis_title="Count", bargap=0.2)
            
            fig_html = fig.to_html(full_html=False)
        print(recommendations[0])

    return render_template('genre.html', inputs=genres,
                           form=form, output=genre_data, 
                           histogram=fig_html, suggestions=recommendations)

@views.route('/track', methods=['GET', 'POST'])
def track():
    track, track_1, track_2, track_3,  form = read_input(InputForm)
    if track:

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

# VERY SLOW, NEEDS A WHOLE REWRITE!!!! - Jonathan Duggan 2024-03-24
def apriori_algorithm(genre):
    filtered_df = artist_info_csv[artist_info_csv["genres"].str.contains(genre.lower(), case=False, na=False)].copy()
    
    filtered_df["genres"] = filtered_df["genres"].apply(lambda x: x.split(', ') if isinstance(x, str) else [])

    items = filtered_df["genres"].tolist()

    encoder = TransactionEncoder()
    encoded_items = encoder.fit_transform(items)
    
    df_sample = pd.DataFrame(encoded_items, columns=encoder.columns_)
    df_sample = df_sample.replace({False: 0, True: 1})  

    print(f'Number of transactions: {len(df_sample)}')
    print(f'Number of items: {len(df_sample.columns)}')
    print(f'Unique items are: {list(df_sample.columns)}')

    support_count = len(df_sample) / 1000
    df_itemset_max_1 = apriori(df_sample, min_support=support_count / len(df_sample), use_colnames=True)
    
    top_list = df_itemset_max_1.head(25)
    top_list["itemsets"] = top_list["itemsets"].apply(lambda x: ', '.join(list(x)) if isinstance(x, (set, tuple)) else x)

    print("KILLER KEEMSTARRRR!! ", top_list)
    
    return top_list.to_html(classes="table table-striped", index=False)
