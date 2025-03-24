from api_utilities import connect_spotify_api
import logging
import json
from dotenv import load_dotenv
from requests import get, post, exceptions
from googleapiclient.discovery import build
from ytmusicapi import YTMusic
import os

class GoogleAPIFacade:
    def __init__(self, API_CLIENT_ID_NAME: str):
        load_dotenv()
        YOUTUBE_API_KEY = os.getenv(API_CLIENT_ID_NAME)
        if YOUTUBE_API_KEY is None:
            logging.error(f"Could not retrieve {API_CLIENT_ID_NAME} "
                           "from .env file")
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        self.ytmusic = YTMusic()
       
    def get_youtube(self):
        return self.youtube
    
    def search_for_video(self, query: str, limit=1, order='relevance'):
        request = self.youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=limit,
            order=order
        )
        response = request.execute()
        return response
    
    def get_video_statistics(self, video_ids: str):
        request = self.youtube.videos().list(
            part='statistics',
            id=",".join(video_ids)
        )
        response = request.execute()
        return response
    
    def get_ytmusic(self):
        return self.ytmusic
    