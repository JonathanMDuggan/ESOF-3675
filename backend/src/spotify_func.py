from api_utilities import load_api
import logging
import json
from dotenv import load_dotenv
from requests import get, post 

class SpotifyAPIInterface:
    def __init__(self, API_CLIENT_ID_NAME, API_CLIENT_SECERT_NAME):
        load_dotenv()
        self.token = load_api(API_CLIENT_ID_NAME, API_CLIENT_SECERT_NAME,
                 "https://accounts.spotify.com/api/token" )
        if self.token == None:
            logging.error("Failed to fetch token from spotify servers")
        else:
            self.auth_header = {"Authorization": "Bearer " + self.token}
        return
    
    def get_artist_by_name(self, artist_name : str):
        URL = "https://api.spotify.com/v1/search"
        QUERY = f'?q={artist_name}&type=artist&limit=1'
        QUERY_URL = URL + QUERY
        headers = self.auth_header
        result = get(QUERY_URL, headers=self.auth_header)
        JSON_RESULT = json.loads(result.content)
        print(JSON_RESULT)
