import json
import os
import random

import numpy as np
from data_viz import plot_boxplot, plot_heatmap, plot_histogram, plot_scatterplot, plot_seaborn_histogram
from genre_scraper import get_genres, load_and_get_genres_into_db
from import_csv import extract_relevant_data_from_tracks, retrieve_csv_data
from mongo_func import MongoDBFacade
from reporting import report_stats_for_albums, report_stats_for_artists, report_stats_for_tracks
from unofficial_youtube_func import UnOfficialYoutubeAPIFacade
from util_func import add_video_stats_to_tracks, extract_album_ids_from_tracks, extract_artist_ids_from_tracks, extract_relavant_album_info_from_details, extract_relavant_artist_info_from_details, extract_relavant_track_info_from_details, extract_relavant_track_info_from_details_youtube, extract_track_details_from_csv, filter_junction_table_data_by_keys_using_db_collection, get_artists_details, get_artists_top_tracks, get_track_ids_to_video_ids_dict, get_video_statistics
from youtube_func import GoogleAPIFacade
from spotify_func import SpotifyAPIFacade
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

database_name = "music"

collection_name_music_video = "music_video"
collection_name_track = "tracks"
collection_name_artist = "artists"
collection_name_album = "albums"
collection_name_genre = "genres"
collection_name_album_genre = "album_genre_link"
collection_name_artist_genre = "artist_genre_link"
collection_name_track_genre = "track_genre_link"
collection_name_artist_track = "artist_track_link"
collection_name_artist_album = "artist_album_link"
collection_raw_data = "raw_data"
collection_name_genre_history = "genre_history"
limit_tracks_per_run = 50


def get_data(insert_data=False):
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "browser.json")
    google_api = GoogleAPIFacade("YOUTUBE_API_KEY")
    spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
    mongodbClient = MongoDBFacade("MONGO_CONNECTION_STRING")
    unoffical_youtube_api = UnOfficialYoutubeAPIFacade(filepath)

    # Get the data from the database

    # mongodbClient.create_collection(database_name, collection_raw_data) if mongodbClient.get_collection(database_name, collection_raw_data) == None else None


    # dataFrameRaw = retrieve_csv_data()
    # dataFrameRaw = dataFrameRaw.dropna()
    # dataFrameRaw = dataFrameRaw.drop_duplicates(subset=['track_id'])
    # dataFrameRaw = dataFrameRaw.reset_index(drop=True)
    # dataFrameRaw = dataFrameRaw.to_dict(orient='records')
    # mongodbClient.insert_many(database_name, collection_raw_data, dataFrameRaw) if insert_data else None

    genre_dict = load_and_get_genres_into_db(mongodbClient, database_name, collection_name_genre)
    if mongodbClient.get_collection(database_name, collection_name_track) == None:
        mongodbClient.create_collection(database_name, collection_name_track)
    if mongodbClient.get_collection(database_name, collection_name_artist) == None:
        mongodbClient.create_collection(database_name, collection_name_artist)
    if mongodbClient.get_collection(database_name, collection_name_album) == None:
        mongodbClient.create_collection(database_name, collection_name_album)

    tracks = mongodbClient.find_many(database_name, collection_name_track, {})
    artists = mongodbClient.find_many(database_name, collection_name_artist, {})
    albums = mongodbClient.find_many(database_name, collection_name_album, {})

    # extract ids from the data
    artist_ids_database = [artist['id'] for artist in artists]
    album_ids_database = [album['id'] for album in albums]
    track_ids_database = [track['id'] for track in tracks]

    # Get the top 5 tracks of the top 5 artists

    ############################################################################################################
    # Get random tracks, below code is commented out because it is not needed for now
    ############################################################################################################
    # top_five_genres = spotify_api.get_available_genre_seeds()
    # random_tracks = spotify_api.get_recommendations([], top_five_genres, [])
    # random_tracks = random_tracks[:10]


    track_ids_from_database = [track['id'] for track in tracks]
    random_tracks = extract_relevant_data_from_tracks(spotify_api, track_ids_from_database, limit_tracks_per_run)
    ############################################################################################################

    # Get the ids of the random tracks
    track_ids = [track['id'] for track in random_tracks]

    # Use the track ids from database to exclude the tracks that are already
    # in the database
    track_ids = list(set(track_ids) - set(track_ids_database))

    # Exclude the tracks that are already in the database
    random_tracks = [track for track in random_tracks
                     if track['id'] in track_ids]
    
#     if len(random_tracks) == 0:
#         tracks_result = mongodbClient.find_many(database_name, collection_name_track, {})
#         artists_result = mongodbClient.find_many(database_name, collection_name_artist, {})
#         albums_result = mongodbClient.find_many(database_name, collection_name_album, {})
#         return {"tracks": tracks_result, "artists": artists_result, "albums": albums_result}

    print("Number of random tracks: ", len(random_tracks))
    #json print tracks
    # print(json.dumps(random_tracks, indent=4))

    # Get a list of dict of artist id and track id
    artist_track_link = [{"artist_id": artist['id'], "track_id": track['id']} for track in random_tracks for artist in track['artists']]
    # Get the artist_track_link from the database
    artist_track_link_database = mongodbClient.find_many(database_name, collection_name_artist_track, {})
    # Filter out the duplicates in the artist_track_link
    artist_track_link = filter_junction_table_data_by_keys_using_db_collection(artist_track_link, artist_track_link_database, "artist_id", "track_id")


    # Get a list of dict of artist id and album id
    artist_album_link = [{"artist_id": artist['id'], "album_id": track['album']['id']} for track in random_tracks for artist in track['artists']]
    # Filter out the duplicates in the artist_album_link
    artist_album_link = [dict(t) for t in {tuple(d.items()) for d in artist_album_link}]
    # Get the artist_album_link from the database
    artist_album_link_database = mongodbClient.find_many(database_name, collection_name_artist_album, {})
    # Filter out the duplicates in the artist_album_link
    artist_album_link = filter_junction_table_data_by_keys_using_db_collection(artist_album_link, artist_album_link_database, "artist_id", "album_id")


    artist_ids = extract_artist_ids_from_tracks(random_tracks)

    # exclude the artist ids that are already in the database
    artist_ids = list(set(artist_ids) - set(artist_ids_database))

    album_ids = extract_album_ids_from_tracks(random_tracks)
    # exclude the album ids that are already in the database
    album_ids = list(set(album_ids) - set(album_ids_database))

    

    artists_details = spotify_api.get_several_artists(artist_ids)

    
    # Get a list of dict of artist id and genre id, genre from spotify api may be different from the genre from everynoise.com
    artist_genre_link = [{ "artist_id": artist['id'], "genre_id": genre_dict.get(genre.lower(), None)} for artist in artists_details for genre in artist['genres']]
    artist_genre_link = [link for link in artist_genre_link if link['genre_id'] != None]
    # Get the artist_genre_link from the database
    artist_genre_link_database = mongodbClient.find_many(database_name, collection_name_artist_genre, {})
    # Filter out the duplicates in the artist_genre_link
    artist_genre_link = filter_junction_table_data_by_keys_using_db_collection(artist_genre_link, artist_genre_link_database, "artist_id", "genre_id")

    ############################################################################################################
    # Get links for track/genre and album/genre from the csv file (only) not from the api
    ############################################################################################################

    track_genre_link = [{"track_id": track['id'], "genre_id": genre_dict.get(track['track_csv']['playlist_genre'].lower(), None)} for track in random_tracks]
    track_genre_link = [link for link in track_genre_link if link['genre_id'] != None]
    # Get the track_genre_link from the database
    track_genre_link_database = mongodbClient.find_many(database_name, collection_name_track_genre, {})
    # Filter out the duplicates in the track_genre_link
    track_genre_link = filter_junction_table_data_by_keys_using_db_collection(track_genre_link, track_genre_link_database, "track_id", "genre_id")

    # Same for album/genre
    album_genre_link = [{"album_id": track['album']['id'], "genre_id": genre_dict.get(track['track_csv']['playlist_genre'].lower(), None)} for track in random_tracks]
    album_genre_link = [link for link in album_genre_link if link['genre_id'] != None]
    # Get the album_genre_link from the database
    album_genre_link_database = mongodbClient.find_many(database_name, collection_name_album_genre, {})
    # Filter out the duplicates in the album_genre_link
    album_genre_link = filter_junction_table_data_by_keys_using_db_collection(album_genre_link, album_genre_link_database, "album_id", "genre_id")

    ############################################################################################################




    artists_info_extracted = extract_relavant_artist_info_from_details(
         artists_details)

    album_details = spotify_api.get_several_albums(album_ids)
    album_info_extracted = extract_relavant_album_info_from_details(
         album_details)

    # # Get the stats for the random tracks
    # random_tracks_details = add_video_stats_to_tracks(random_tracks, google_api)

        # extract the relevant track info
#     tracks_info_extracted = extract_relavant_track_info_from_details_youtube(
#          random_tracks_details)

    # Use random_tracks_details to get stats about corresponding music video from google api
    track_ids_to_video_ids_dict = get_track_ids_to_video_ids_dict(random_tracks, google_api, unofficial_youtube_api=unoffical_youtube_api)

    video_statistics_dict = get_video_statistics(track_ids_to_video_ids_dict, google_api)

    # Get the existing video statistics from database
    existing_video_statistics = mongodbClient.find_many(database_name, collection_name_music_video, {})
    existing_video_statistics_id_set = set([video['track_id'] for video in existing_video_statistics])
    # Filter out the video statistics that are already in the database
    video_statistics_dict = {track_id: video_statistics for track_id, video_statistics in video_statistics_dict.items() if track_id not in existing_video_statistics_id_set}

    ############################################################################################################
    # Extract final info for tracks
    ############################################################################################################
    # tracks_info_extracted = extract_relavant_track_info_from_details(random_tracks)
    tracks_info_extracted = extract_track_details_from_csv(random_tracks)
    ############################################################################################################

    # Insert the data into the database
    if insert_data:
        mongodbClient.create_database(database_name)
        mongodbClient.create_collection(database_name, collection_name_track)
        mongodbClient.create_collection(database_name, collection_name_artist)
        mongodbClient.create_collection(database_name, collection_name_album)

        mongodbClient.insert_many(database_name,
                                  collection_name_track, 
                                   tracks_info_extracted) if len(tracks_info_extracted) > 0 else None
        mongodbClient.insert_many(database_name, 
                                  collection_name_artist,
                                  artists_info_extracted) if len(artists_info_extracted) > 0 else None
        mongodbClient.insert_many(database_name, collection_name_album, 
                                  album_info_extracted) if len(album_info_extracted) > 0 else None
        
        mongodbClient.create_collection(database_name, collection_name_music_video) if mongodbClient.get_collection(database_name, collection_name_music_video) == None else None
        mongodbClient.insert_many(database_name, collection_name_music_video, video_statistics_dict.values()) if len(video_statistics_dict) > 0 else None
        
        # Create and insert the genre junction collections data
        # for now we are only inserting the artist_genre_link
        # since Spotify API does not provide genre information for albums and tracks
        mongodbClient.create_collection(database_name, collection_name_artist_genre) if mongodbClient.get_collection(database_name, collection_name_artist_genre) == None else None
        mongodbClient.create_collection(database_name, collection_name_album_genre) if mongodbClient.get_collection(database_name, collection_name_album_genre) == None else None
        mongodbClient.create_collection(database_name, collection_name_track_genre) if mongodbClient.get_collection(database_name, collection_name_track_genre) == None else None


        mongodbClient.insert_many(database_name, collection_name_artist_genre, artist_genre_link) if len(artist_genre_link) > 0 else None
        mongodbClient.insert_many(database_name, collection_name_album_genre, album_genre_link) if len(album_genre_link) > 0 else None
        mongodbClient.insert_many(database_name, collection_name_track_genre, track_genre_link) if len(track_genre_link) > 0 else None

        # Create and insert the artist_track_link and artist_album_link
        mongodbClient.create_collection(database_name, collection_name_artist_track) if mongodbClient.get_collection(database_name, collection_name_artist_track) == None else None
        mongodbClient.create_collection(database_name, collection_name_artist_album) if mongodbClient.get_collection(database_name, collection_name_artist_album) == None else None
        
        mongodbClient.insert_many(database_name, collection_name_artist_track, artist_track_link) if len(artist_track_link) > 0 else None
        mongodbClient.insert_many(database_name, collection_name_artist_album, artist_album_link) if len(artist_album_link) > 0 else None


    # mongodbClient.delete_many(database_name, collection_name_track, {})
    # mongodbClient.delete_many(database_name, collection_name_artist, {})
    # mongodbClient.delete_many(database_name, collection_name_album, {})

    return {"tracks": tracks_info_extracted,
            "artists": artists_info_extracted,
            "albums": album_info_extracted}


def process_data_from_db(data=None):
     mongodbClient = MongoDBFacade("MONGO_CONNECTION_STRING")


     # Get the data from the database
     tracks = mongodbClient.find_many(
          database_name, 
          collection_name_track, {}) #if data == None else data['tracks']
     artists = mongodbClient.find_many(
          "music", 
          collection_name_artist, {}) #if data == None else data['artists']
     albums = mongodbClient.find_many(
          "music",
          collection_name_album, {}) #if data == None else data['albums']
     

     # # Convert the data to dataframes
     # tracks_df = pd.DataFrame(tracks).fillna(value=np.nan)
     # artists_df = pd.DataFrame(artists).fillna(value=np.nan)
     # albums_df = pd.DataFrame(albums).fillna(value=np.nan)


     # # Get the shape of the Dataframes
     # print("Shape of the tracks dataframe")
     # print(tracks_df.shape)
     # print("Shape of the artists dataframe")
     # print(artists_df.shape)
     # print("Shape of the albums dataframe")
     # print(albums_df.shape)

     # # Get the statistical summary of the Dataframes
     # print("Statistical summary of the tracks dataframe")
     # print(tracks_df.describe())
     # print("Statistical summary of the artists dataframe")
     # print(artists_df.describe())
     # print("Statistical summary of the albums dataframe")
     # print(albums_df.describe())

     # # Get the info of the Dataframes
     # print("Info of the tracks dataframe")
     # print(tracks_df.info())
     # print("Info of the artists dataframe")
     # print(artists_df.info())
     # print("Info of the albums dataframe")
     # print(albums_df.info())

     # Get the stats for the data

     # report_stats_for_tracks(tracks_df)
     # report_stats_for_artists(artists_df)
     # report_stats_for_albums(albums_df)

     # plot_boxplot(tracks_df, "popularity")
     # plot_boxplot(artists_df, "popularity")
     # plot_boxplot(albums_df, "popularity")

     # tracks_df = tracks_df.dropna()
     # artists_df = artists_df.dropna()
     # albums_df = albums_df.dropna()

     # tracks_drop_columns = ["_id", "id", "video_id", "video_name", "name", "explicit", "release_date", "release_date_precision"]
     # artists_drop_columns = ["_id", "id", "name"]
     # albums_drop_columns = ["_id", "id", "name", "release_date", "release_date_precision"]

     # tracks_df = tracks_df.drop(columns=tracks_drop_columns)
     # artists_df = artists_df.drop(columns=artists_drop_columns)
     # albums_df = albums_df.drop(columns=albums_drop_columns)

     # plot_heatmap(tracks_df)
     # plot_heatmap(artists_df)
     # plot_heatmap(albums_df)

     # plot_scatterplot(tracks_df, "popularity", "view_count")
     # plot_scatterplot(tracks_df, "popularity", "like_count")
     # plot_scatterplot(tracks_df, "popularity", "comment_count")
     # plot_scatterplot(tracks_df, "popularity", "duration_ms")
     # plot_scatterplot(tracks_df, "popularity", "track_number")

     # plot_histogram(tracks_df, "popularity", 20)
     # plot_seaborn_histogram(tracks_df, "popularity")










    