import os

import numpy as np
from mongo_func import MongoDBFacade
from reporting import report_stats_for_albums, report_stats_for_artists, report_stats_for_tracks
from util_func import add_video_stats_to_tracks, extract_album_ids_from_tracks, extract_artist_ids_from_tracks, extract_relavant_album_info_from_details, extract_relavant_artist_info_from_details, extract_relavant_track_info_from_details, extract_relavant_track_info_from_details_2, extract_relavant_track_info_from_details_youtube, get_artists_details, get_artists_top_tracks
from youtube_func import GoogleAPIFacade
from spotify_func import SpotifyAPIFacade
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency


def get_data(insert_data=False):

    google_api = GoogleAPIFacade("YOUTUBE_API_KEY")
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
    mongodbClient = MongoDBFacade("MONGO_CONNECTION_STRING")

    # Get the data from the database
    tracks = mongodbClient.find_many("music", "sample_tracks", {})
    artists = mongodbClient.find_many("music", "sample_artists", {})
    albums = mongodbClient.find_many("music", "sample_albums", {})

    # extract ids from the data
    artist_ids_database = [artist['id'] for artist in artists]
    album_ids_database = [album['id'] for album in albums]
    track_ids_database = [track['id'] for track in tracks]

    # Get the top 5 tracks of the top 5 artists

    top_five_genres = spotify_api.get_available_genre_seeds()

    random_tracks = spotify_api.get_recommendations([], top_five_genres, [])
    random_tracks = random_tracks[:5]

    artist_ids = extract_artist_ids_from_tracks(random_tracks)
    # exclude the artist ids that are already in the database
    artist_ids = list(set(artist_ids) - set(artist_ids_database))

    album_ids = extract_album_ids_from_tracks(random_tracks)
    # exclude the album ids that are already in the database
    album_ids = list(set(album_ids) - set(album_ids_database))

    # Get the ids of the random tracks
    track_ids = [track['id'] for track in random_tracks]

    # Use the track ids from database to exclude the tracks that are already
    # in the database
    track_ids = list(set(track_ids) - set(track_ids_database))

    # Remove tracks from random_tracks that are already in the database
    random_tracks = [track for track in random_tracks
                     if track['id'] in track_ids]

    artists_details = spotify_api.get_several_artists(artist_ids)
    artists_info_extracted = extract_relavant_artist_info_from_details(
         artists_details)

    album_details = spotify_api.get_several_albums(album_ids)
    album_info_extracted = extract_relavant_album_info_from_details(
         album_details)

    # Get the stats for the random tracks
    random_tracks_details = add_video_stats_to_tracks(random_tracks, google_api)

    # extract the relevant track info
    tracks_info_extracted = extract_relavant_track_info_from_details_youtube(
         random_tracks_details)


    # Insert the data into the database
    if insert_data:
        mongodbClient.create_database("music")
        mongodbClient.create_collection("music", "sample_tracks")
        mongodbClient.create_collection("music", "sample_artists")
        mongodbClient.create_collection("music", "sample_albums")
        mongodbClient.insert_many("music",
                                  "sample_tracks", 
                                   tracks_info_extracted)
        mongodbClient.insert_many("music", 
                                  "sample_artists",
                                  artists_info_extracted)
        mongodbClient.insert_many("music", "sample_albums", 
                                  album_info_extracted)

    # mongodbClient.delete_many("music", "sample_tracks", {})
    # mongodbClient.delete_many("music", "sample_artists", {})
    # mongodbClient.delete_many("music", "sample_albums", {})

    return {"tracks": tracks_info_extracted,
            "artists": artists_info_extracted,
            "albums": album_info_extracted}


def process_data_from_db(data=None):
        mongodbClient = MongoDBFacade("MONGO_CONNECTION_STRING")

        # Get the data from the database
        tracks = mongodbClient.find_many(
             "music", 
             "sample_tracks", {}) if data == None else data['tracks']
        artists = mongodbClient.find_many(
             "music", 
             "sample_artists", {}) if data == None else data['artists']
        albums = mongodbClient.find_many(
             "music",
             "sample_albums", {}) if data == None else data['albums']

        # Convert the data to dataframes
        tracks_df = pd.DataFrame(tracks).fillna(value=np.nan)
        artists_df = pd.DataFrame(artists).fillna(value=np.nan)
        albums_df = pd.DataFrame(albums).fillna(value=np.nan)


        # Get the shape of the Dataframes
        print("Shape of the tracks dataframe")
        print(tracks_df.shape)
        print("Shape of the artists dataframe")
        print(artists_df.shape)
        print("Shape of the albums dataframe")
        print(albums_df.shape)

        # Get the statistical summary of the Dataframes
        print("Statistical summary of the tracks dataframe")
        print(tracks_df.describe())
        print("Statistical summary of the artists dataframe")
        print(artists_df.describe())
        print("Statistical summary of the albums dataframe")
        print(albums_df.describe())

        # Get the info of the Dataframes
        print("Info of the tracks dataframe")
        print(tracks_df.info())
        print("Info of the artists dataframe")
        print(artists_df.info())
        print("Info of the albums dataframe")
        print(albums_df.info())

        # Get the stats for the data

        report_stats_for_tracks(tracks_df)
        report_stats_for_artists(artists_df)
        report_stats_for_albums(albums_df)










    