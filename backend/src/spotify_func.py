from api_utilities import connect_spotify_api
import logging
import json
from dotenv import load_dotenv
from requests import get, post, exceptions

class SpotifyAPIFacade:
    def __init__(self, API_CLIENT_ID_NAME, API_CLIENT_SECRET_NAME):
        self.URL_SEARCH = "https://api.spotify.com/v1/search"
        self.search_types = ["album", "artist", "playlist", "track", 
                            "show", "episode", "audiobook"]
        load_dotenv()
        self.token = connect_spotify_api(API_CLIENT_ID_NAME, API_CLIENT_SECRET_NAME,
                 "https://accounts.spotify.com/api/token" )
        if self.token is None:
            logging.error("Failed to fetch token from spotify servers")
        else:
            self.auth_header = {"Authorization": "Bearer " + self.token}
        return
    
    def print_json_from_query(self, QUERY: str):
       QUERY_URL = self.URL_SEARCH + QUERY
       try:
           response = get(QUERY_URL, headers=self.auth_header)
           JSON_RESULT = json.loads(response.content)
       except exceptions.RequestException as e:
           logging.error(f"Request Failed: {e}") 
       print(JSON_RESULT)

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
        self.print_json_from_query(QUERY)

    def get_artists_top_tracks(id: str):
        pass