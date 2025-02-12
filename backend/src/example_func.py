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
import numpy as np


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

def ExplicitExample():
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")

def popularity_example():
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
        # Pass the artist ID to the get_artist_top_tracks function
    rap = spotify_api.search_for_item("track", None , 50, "genre%3Arap")
    vapor_wave = spotify_api.search_for_item("track", None , 50, "genre%3Avaporwave")
    pop = spotify_api.search_for_item("track", None , 50, "genre%pop")
    electroacoustic_improvisation = spotify_api.search_for_item("track", None , 50, "genre%3AElectroacoustic+Improvisation")

    rap_list = list(map(lambda x: {
        "name": x['name'], 
        "popularity": x['popularity']},
        rap))
    vapor_wave_list = list(map(lambda x: {
        "name": x['name'], 
        "popularity": x['popularity']},
        vapor_wave))
    
    rap_panda = pd.DataFrame(rap_list)
    vapor_panda  = pd.DataFrame(vapor_wave_list)

        # Create the Horizontal Bar Graphs
    fig, ax = plt.subplots()
    ax.barh(rap_panda['name'], rap_panda['popularity'])
    ax.set_ylabel('popularity')
    ax.set_title('Rap popularity')
    
    fig, ax = plt.subplots()
    ax.barh(vapor_panda['name'], vapor_panda['popularity'])
    ax.set_ylabel('popularity')
    ax.set_title('Vaporwave popularity')

    # Visualize the Data
    plt.show()
    

def duration_distribution_example():
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
    pop = spotify_api.search_for_item("track", None , 50, "genre%3Agospel")
    pop_list = list(map(lambda x: {
        "duration_ms": x['duration_ms']},
    pop))
    
    pop_panda = pd.DataFrame(pop_list)
    plt.hist(pop_panda, color='lightgreen', ec='black', bins=50)
    plt.title("Gospel Duration in Milliseconds")
    plt.xlabel("Time")
    plt.show()

def box_plot():
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")

    rap = spotify_api.search_for_item("track", None , 50, "genre%3Arap")
    vapor_wave = spotify_api.search_for_item("track", None , 50, "genre%3Avaporwave")
    pop = spotify_api.search_for_item("track", None , 50, "genre%pop")
    acid_jazz = spotify_api.search_for_item("track", None , 50, "genre%3Aacid+jazz")
    labels = ['rap' , 'vapor_wave' , 'pop' , 'acid jazz']
    colors = ['peachpuff', 'orange', 'tomato', 'blue']

    rap_list = list(map(lambda x: {
        x['popularity']},
       rap))
    vapor_wave_list = list(map(lambda x: {
        x['popularity']},
       vapor_wave))
    pop_list = list(map(lambda x: {
       x['popularity']},
       pop))
    jazz_list = list(map(lambda x: {
        x['popularity']},
       acid_jazz))
    

    rap_list = pd.DataFrame(rap_list).to_numpy().flatten()
    vapor_wave_list = pd.DataFrame(vapor_wave_list).to_numpy().flatten()
    pop_list = pd.DataFrame(pop_list).to_numpy().flatten()
    jazz_list = pd.DataFrame(jazz_list).to_numpy().flatten()

    weights = [
        rap_list,
        vapor_wave_list,
        pop_list,
        jazz_list
    ]

    fig, ax = plt.subplots()
    ax.set_ylabel('popularity')
    
    bplot = ax.boxplot(weights,
                   patch_artist=True,  # fill with color
                   tick_labels=labels)  # will be used to label x-ticks
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    plt.title("Box Plot of Genre Popularity")
    plt.ylabel("Popularity")
    plt.show()

def correlation():
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
    rappers = spotify_api.search_for_item("artist", None , 50, "genre%3Arap")
    x = list(map(lambda x: {
        x['popularity']},
    rappers))

    y = list(map(lambda x: { x['followers']['total']}, rappers))
    x = pd.DataFrame(x)
    y = pd.DataFrame(y)
    x = x.to_numpy().flatten()
    y = y.to_numpy().flatten()
    plt.scatter(y, x)
    print("hello")
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))
         (np.unique(x)), color='red')
    plt.title(f"Scatter Plot of Popularity and Followers for Rappers")
    plt.ylabel(f"Followers")
    plt.xlabel(f"Popularity")
    plt.show()



