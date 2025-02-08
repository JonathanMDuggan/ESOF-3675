from api_utilities import load_api
import logging
import json
from dotenv import load_dotenv
from requests import get, post 

class SpotifyAPIFacade:
    def __init__(self, API_CLIENT_ID_NAME, API_CLIENT_SECRET_NAME):
        self.URL_SEARCH = "https://api.spotify.com/v1/search"
        load_dotenv()
        self.token = load_api(API_CLIENT_ID_NAME, API_CLIENT_SECRET_NAME,
                 "https://accounts.spotify.com/api/token" )
        if self.token == None:
            logging.error("Failed to fetch token from spotify servers")
        else:
            self.auth_header = {"Authorization": "Bearer " + self.token}
        return
    
    def print_json_from_query(self, QUERY: str):
       QUERY_URL = self.URL_SEARCH + QUERY
       result = get(QUERY_URL, headers=self.auth_header)
       JSON_RESULT = json.loads(result.content)
       print(JSON_RESULT)

    # For information about the search functionality you can read more here
    # https://developer.spotify.com/documentation/web-api/reference/search

    # Uses the search functionality to find the most popular artist by name    
    def get_artist_by_name(self, artist_name : str):
        QUERY = f'?q={artist_name}&type=artist&limit=1'
        self.print_json_from_query(QUERY)

    # Uses the search functionality to find the related artists by name
    def get_artist_list_by_name(self, artist_name: str, number: int):
       if number <= 0:
           logging.warning("We cannot create a list less than or equal to 0")
           return
       QUERY = f'?q={artist_name}&type=artist&limit={number}'
       self.print_json_from_query(QUERY)
    
    # Uses the search functionality to find the most popular album by name
    def get_album_by_name(self, album_name : str):
        QUERY = f'?q={album_name}&type=album&limit=1'
        self.print_json_from_query(QUERY)

    # Uses the search functionality to find the related albums by name
    def get_album_list_by_name(self, album_name : str, number: int):
        if number <= 0:
           logging.warning("We cannot create a list less than or equal to 0")
           return
        QUERY = f'?q={album_name}&type=album&limit={number}'
        self.print_json_from_query(QUERY)

    # Uses the search functionality to find the most popular track by name
    def get_track_by_name(self, track_name : str):
        QUERY = f'?q={track_name}&type=track&limit=1'
        self.print_json_from_query(QUERY)

    # Uses the search functionality to find the most popular track by name
    def get_track_list_by_name(self, track_name : str, number: int):
        if number <= 0:
           logging.warning("We cannot create a list less than or equal to 0")
           return
        QUERY = f'?q={track_name}&type=track&limit={number}'
        self.print_json_from_query(QUERY)