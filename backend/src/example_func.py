import os
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



def OutlierExample():
    # Connect to the spotify api
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
    

    # Pass the artist ID to the get_artist_top_tracks function
    the_weeknd_tracks = spotify_api.get_artist_top_tracks(
        spotify_api.name_to_id_adapter("artist", "The Weeknd")
    )
    gotye_tracks = spotify_api.get_artist_top_tracks(
        spotify_api.name_to_id_adapter("artist", "Gotye")
    )

    # Store the top songs in a list with name and popularity as the dimensions 
    the_weeknd_track_names_and_pop = list(map(lambda x: {
        "name": x['name'], 
        "popularity": x['popularity']},
        the_weeknd_tracks['tracks']))
    gotye_track_names_and_pop = list(map(lambda x: {
        "name": x['name'], 
        "popularity": x['popularity']},
        gotye_tracks['tracks']))
    
    # Transform the data into a panda DataFrame
    weeknd_panda = pd.DataFrame(the_weeknd_track_names_and_pop)
    gotye_panda  = pd.DataFrame(gotye_track_names_and_pop)


    # Create the Horizontal Bar Graphs
    fig, ax = plt.subplots()
    ax.barh(weeknd_panda['name'], weeknd_panda['popularity'])
    ax.set_ylabel('popularity')
    ax.set_title('The Weeknd: Top Songs')
    
    fig, ax = plt.subplots()
    ax.barh(gotye_panda['name'], gotye_panda['popularity'])
    ax.set_ylabel('popularity')
    ax.set_title('Gotye: Top Songs')

    # Visualize the Data
    plt.show()