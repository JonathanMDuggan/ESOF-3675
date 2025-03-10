import json

import numpy as np
from spotify_func import SpotifyAPIFacade
from youtube_func import GoogleAPIFacade


def get_artists_details(artist_names: list, 
                        spotify_api: SpotifyAPIFacade) -> list:
    """
    This function takes in a list of artist names and a SpotifyAPIFacade object
    and returns a list of dictionaries containing the artist's name, id, 
    and popularity.
    """
    artist_details = []
    for artist_name in artist_names:
        response = spotify_api.search_for_item("artist", artist_name, 1)
        if response:
            artist_details.append({"name": response[0]['name'],
                                   "id": response[0]['id'],
                                   "popularity": response[0]['popularity']})
    return artist_details


def get_artist_top_tracks(artist_id: str,
                          spotify_api: SpotifyAPIFacade) -> list:
    """
    This function takes in an artist id and a SpotifyAPIFacade object
    and returns a list of dictionaries containing the track's name, id, and
    popularity.
    """
    response = spotify_api.get_artist_top_tracks(artist_id)
    if response:
        return [{"name": track['name'],
                 "id": track['id'], 
                 "popularity": track['popularity']}
                 for track in response['tracks']]
    return []

def get_artists_top_tracks(artist_names: list,
                           spotify_api: SpotifyAPIFacade) -> list:
    """
    This function takes in a list of artist names and a SpotifyAPIFacade object
    and returns a list of dictionaries containing the artist's name, id, 
    popularity, and their top tracks.
    """
    artists_details = get_artists_details(artist_names, spotify_api)
    for artist in artists_details:
        artist['top_tracks'] = get_artist_top_tracks(artist['id'], spotify_api)
    return artists_details

def add_video_stats_to_tracks(artists_top_tracks: list,
                              google_api: GoogleAPIFacade) -> list:
    """
    This function takes in a list of artists' top tracks and a
    GoogleAPIFacade object and returns a list of dictionaries containing the
    artist's name, id, popularity, and their top tracks with video statistics.
    """
    for artist in artists_top_tracks:
        for track in artist['top_tracks']:
            response = google_api.search_for_video(
                track['name'], 1, 'viewCount')
            if response:
                video_id = response['items'][0]['id']['videoId']
                response = google_api.get_video_statistics(video_id)
                track['video_statistics'] = response['items'][0]['statistics']
    return artists_top_tracks

def extract_artist_ids_from_tracks(tracks: list) -> list:
    """
    This function takes in a list of tracks and returns a list of
    unique artist ids.
    """
    artist_ids = set()
    for track in tracks:
        artist_ids.add(track['artists'][0]['id'])
    return list(artist_ids)

def extract_album_ids_from_tracks(tracks: list) -> list:
    """
    This function takes in a list of tracks and returns a list of 
    unique album ids.
    """
    album_ids = set()
    for track in tracks:
        album_ids.add(track['album']['id'])
    return list(album_ids)


def add_video_stats_to_tracks(tracks: list, google_api: GoogleAPIFacade) -> list:
    """
    This function takes in a list of tracks and a GoogleAPIFacade object
    and returns a list of dictionaries containing the track's name, id, 
    popularity, and video statistics.
    """
    for track in tracks:
        response = google_api.search_for_video(f'{track['artists'][0]['name']} - {track['name']}', 1, 'relevance')
        if response:
            video_id = response['items'][0]['id']['videoId']
            video_name = response['items'][0]['snippet']['title']
            response = google_api.get_video_statistics(video_id)
            track['video_id'] = video_id
            track['video_name'] = video_name
            track['statistics'] = response['items'][0]['statistics']
    return tracks


def extract_relavant_artist_info_from_details(artist_detail_list: list) -> list:
    """
    This function takes in a list of artist details and returns a list of
    dictionaries containing the artist's name, id, and popularity.
    """
    # print(json.dumps(artist_detail_list, indent=4))
    return [{"name": artist['name'], 
             "id": artist['id'],
             "popularity": artist['popularity'],
             "total_followers": artist['followers']['total'] } 
             for artist in artist_detail_list]


def extract_relavant_track_info_from_details(track_detail_list: list) -> list:
    """
    This function takes in a list of track details and returns a 
    list of dictionaries containing the track's name, id, and popularity.
    """
    # print(json.dumps(track_detail_list, indent=4))
    return [{"name": track['name'],
             "id": track['id'], 
             "popularity": track['popularity']}
             for track in track_detail_list]

def extract_relavant_track_info_from_details_youtube(
        track_detail_list: list) -> list:
    """
    This function takes in a list of track details returned from 
    'add_video_stats_to_tracks' and returns a list of dictionaries
     containing the track's name, id, and popularity.
    """
    # print(json.dumps(track_detail_list, indent=4))
    return [{"name": track['name'], 
             "id": track['id'], 
             "popularity": track['popularity'],
             "video_id": track['video_id'], 
             "video_name": track['video_name'], 
             "view_count": track['statistics'].get('viewCount', None),
             "like_count": track['statistics'].get('likeCount', None),
             "comment_count": track['statistics'].get('commentCount', None),
             "duration_ms": track['duration_ms'],
             "release_date": track['album']['release_date'] or "1970-01-01",
             "release_date_precision": track['album']['release_date_precision'],
             "explicit": track['explicit'],
             "track_number": track['track_number'],
            } for track in track_detail_list]


def extract_relavant_album_info_from_details(album_detail_list: list) -> list:
    """
    This function takes in a list of album details and returns a list of 
    dictionaries containing the album's name, id, and popularity.
    """
    # print(json.dumps(album_detail_list, indent=4))
    return [{"name": album['name'], 
             "id": album['id'],
             "popularity": album['popularity'],
             "total_tracks": album['total_tracks'],
             "release_date": album['release_date'],
             "release_date_precision": album['release_date_precision']}
              for album in album_detail_list]