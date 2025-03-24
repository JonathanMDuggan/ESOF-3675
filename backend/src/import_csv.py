import random
import pandas as pd
import os


from spotify_func import SpotifyAPIFacade

file1 = "archive/high_popularity_spotify_data.csv"
file2 = "archive/low_popularity_spotify_data.csv"
columns = ["energy","tempo","danceability","playlist_genre","loudness","liveness","valence","track_artist","time_signature","speechiness","track_popularity","track_href","uri","track_album_name","playlist_name","analysis_url","track_id","track_name","track_album_release_date","instrumentalness","track_album_id","mode","key","duration_ms","acousticness","id","playlist_subgenre","type","playlist_id"]


def import_csv(file):
    data = pd.read_csv(file)
    return data

def retrieve_csv_data():
    dirname = os.path.dirname(__file__)
    filename1 = os.path.join(dirname, file1)
    filename2 = os.path.join(dirname, file2)
    data1 = import_csv(filename1)
    data2 = import_csv(filename2)
    return pd.concat([data1, data2], ignore_index=True)

def extract_relevant_data_from_tracks(spotifyFacade: SpotifyAPIFacade, database_track_ids: list, limit_tracks_per_run: int = 50):
    data = retrieve_csv_data()
    list_dict =  data[columns].to_dict(orient='records')
    list_dict = list(filter(lambda x: x['track_id'] != 'None', list_dict))
    list_dict = list(filter(lambda x: x['track_id'] not in database_track_ids, list_dict))
    random.shuffle(list_dict)
    max_limit = min(limit_tracks_per_run - 1, len(list_dict))
    list_dict =  list_dict[:max_limit]
    list_dict_ids = []
    for i in list_dict:
        list_dict_ids.append(i['track_id'])
    list_dict_ids = list(set(list_dict_ids))
    spotify_tracks = spotifyFacade.get_several_tracks(list_dict_ids)
    spotify_tracks_dict = {}
    for i in spotify_tracks:
        spotify_tracks_dict[i['id']] = i
    list_results = []
    for i in list_dict:
        list_results.append({**spotify_tracks_dict[i['track_id']],
             'track_csv': i})
    return list_results



