from api_utilities import connect_spotify_api
import logging
import json
from dotenv import load_dotenv
from requests import get, post, exceptions
from googleapiclient.discovery import build
import os

class YoutubeAPIFacade:
    def __init__(self, API_CLIENT_ID_NAME):
        load_dotenv()
        API_KEY = os.getenv(API_CLIENT_ID_NAME)
        self.service = build('youtube', 'v3', developerKey=API_KEY)
        pass
