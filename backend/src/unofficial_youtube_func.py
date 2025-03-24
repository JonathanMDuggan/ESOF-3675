import logging
import json
from dotenv import load_dotenv
from requests import get, post, exceptions
from ytmusicapi import YTMusic
import os

class UnOfficialYoutubeAPIFacade:
    def __init__(self, browser_file: str):
        self.ytmusic = YTMusic(browser_file)
       
    def get_youtube(self):
        return self.ytmusic
    
    def search_for_video(self, query: str, limit=1, order='relevance'):
        search_results = self.ytmusic.search(query, filter="videos", limit=limit)
        return search_results if search_results else None
    
    def get_video_statistics(self, video_id: str):
        return self.ytmusic.get_song(video_id)