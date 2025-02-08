from src.main import load_api
import logging
from dotenv import load_dotenv

class SpotifyAPI:
    def __init__(self, API_CLIENT_ID_NAME, API_CLIENT_SECERT_NAME):
        load_dotenv()
        self.token = load_api(API_CLIENT_ID_NAME, API_CLIENT_SECERT_NAME,
                 "https://accounts.spotify.com/api/token" )
        if self.token == None:
            logging.error("Failed to fetch token from spotify servers")
        else:
            self.auth_header = {"Authorization": "Bearer " + self.token}
        return
    
    def get_artist(artist_name : str):
        pass