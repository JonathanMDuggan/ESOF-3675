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


    # Uses the search functionality to find the related types by name  
    def get_type_by_name(self, type : str, type_name: str, limit=1):
        if limit <= 0:
            logging.error("The limit cannot be less than 1")
        QUERY = f'?q={type_name}&type={type}&limit={limit}'
        self.print_json_from_query(QUERY)
  