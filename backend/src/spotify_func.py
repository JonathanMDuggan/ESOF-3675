import random
from api_utilities import connect_spotify_api
import logging
import json
from dotenv import load_dotenv
from requests import get, post, exceptions
#from urllib import urlencode

class SpotifyAPIFacade:
    def __init__(self, API_CLIENT_ID_NAME, API_CLIENT_SECRET_NAME):
        self.URL_SEARCH = "https://api.spotify.com/v1/search"
        self.BASE_URL = "https://api.spotify.com/v1"
        self.search_types = ["album", "artist", "playlist", "track", 
                            "show", "episode", "audiobook"]
        load_dotenv()
        self.token = connect_spotify_api(API_CLIENT_ID_NAME,
                                         API_CLIENT_SECRET_NAME,
                 "https://accounts.spotify.com/api/token" )
        if self.token is None:
            logging.error("Failed to fetch token from spotify servers")
        else:
            self.auth_header = {"Authorization": "Bearer " + self.token}
        return
    
    def json_from_query(self, endpoint: str, QUERY: str):
       QUERY_URL = f'{self.BASE_URL}/{endpoint}/{QUERY}'
       try:
           response = get(QUERY_URL, headers=self.auth_header)
           JSON_RESULT = json.loads(response.content)
       except exceptions.RequestException as e:
           logging.error(f"Request Failed: {e}") 
    #    print(JSON_RESULT)
       return JSON_RESULT

    # For information about the search functionality you can read more here
    # https://developer.spotify.com/documentation/web-api/reference/search
    # Uses the search functionality to find the related types by name  
    def search_for_item(self, type : str, type_name: str, limit=1):
        if type not in self.search_types:
            logging.error(f"Type {type} is not a valid parameter")
            return
        if limit <= 0:
            logging.error("The limit cannot be less than 1")
            return
        QUERY = f'?q={type_name}&type={type}&limit={limit}'
        result = self.json_from_query("search", QUERY)
        return result[f'{type}s']['items']
    
    # Returns the most popular type id from type name 
    def name_to_id_adapter(self, type: str, type_name: str) -> str:
        result = self.search_for_item(type, type_name)
        return result[0]['id']

    def get_track(self, track_id):
        if track_id == None:
            logging.error("Track ID cannot be None")
            return
        QUERY = f'{track_id}'
        result = self.json_from_query("tracks", QUERY)
        return result
    
    def get_artist_top_tracks(self, artist_id):
        if artist_id == None:
            logging.error("Artist ID cannot be None")
            return
        QUERY = f'{artist_id}/top-tracks'
        result = self.json_from_query("artists", QUERY)
        return result
    
    def get_available_genre_seeds(self):
        """ deprecated API endpoint """
        QUERY = "recommendations/available-genre-seeds"
        QUERY_URL = f'{self.BASE_URL}/{QUERY}'
        genres = ["alternative","samba", "rock", "pop", "rap", "jazz",
                  "hip-hop", "country", "blues", "classical", "dance",
                  "disco", "electronic", "folk"]
        genres = random.sample(genres, 5)
        return genres
    
    def get_recommendations(self, seed_artists: list, 
                            seed_genres: list, seed_tracks: list):
        """ deprecated API endpoint """
        return self.search_for_item("track", f'{seed_genres[0]}{seed_genres[1]}'
                                    ,50)
    
    def get_several_artists(self, artist_ids: list):
        if artist_ids == None:
            logging.error("Artist IDs cannot be None")
            return
        QUERY = f'?ids={",".join(artist_ids)}'
        result = self.json_from_query("artists", QUERY)
        return result['artists']
    
    def get_several_tracks(self, track_ids: list):
        if track_ids == None:
            logging.error("Track IDs cannot be None")
            return
        QUERY = f'?ids={",".join(track_ids)}'
        result = self.json_from_query("tracks", QUERY)
        return result['tracks']
    
    def get_several_albums(self, album_ids: list):
        if album_ids == None:
            logging.error("Album IDs cannot be None")
            return
        QUERY = f'?ids={",".join(album_ids)}'
        result = self.json_from_query("albums", QUERY)
        return result['albums']
    
    def get_artist_albums(self, artist_id: str, limit=20):
        if artist_id == None:
            logging.error("Artist ID cannot be None")
            return
        if 1 <= limit >= 50:
            QUERY = f'{artist_id}/albums?limit={limit}'
        else:
            logging.error("The limit must be between 1 and 50")
            return
        result = self.json_from_query("albums", QUERY)
        return result['albums']

    def get_album_tracks(self, album_id: str, limit=20):
        if album_id == None:
            logging.error("Album ID cannot be None")
            return
        
        

    def get_artist_album_tracks(self, artist_id: str, limit=20):
        if artist_id == None:
            logging.error("Artist IDs cannot be None")
            return
        albums = self.get_artist_albums(artist_id, limit)


        

    
