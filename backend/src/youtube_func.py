from api_utilities import connect_spotify_api
import logging
import json
from dotenv import load_dotenv
from requests import get, post, exceptions
from googleapiclient.discovery import build
import os

class GoogleAPIFacade:
    def __init__(self, API_CLIENT_ID_NAME: str):
        load_dotenv()
        YOUTUBE_API_KEY = os.getenv(API_CLIENT_ID_NAME)
        if YOUTUBE_API_KEY is None:
            logging.error(f"Could not retrieve {API_CLIENT_ID_NAME} "
                           "from .env file")
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
       
    def get_youtube(self):
        return self.youtube