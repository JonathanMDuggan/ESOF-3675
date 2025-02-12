import os
from data_collect import get_data, process_data_from_db
from youtube_func import GoogleAPIFacade
from spotify_func import SpotifyAPIFacade
from flask import Flask, render_template, request, jsonify
import logging
from requests import post
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<home>')
def name():
    return 'You typed home in the funny thing <home>'

def main():
    # # Set the logging level to its lowest level
    # google_api = GoogleAPIFacade("YOUTUBE_API_KEY")
    # spotify_api = SpotifyAPIFacade("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET")
    # spotify_api.search_for_item("track", "Beat it")
    # youtube = google_api.get_youtube()
    # #request = youtube.channels().list(
    #     #part='statistics',
    #     #forUsername='sentdex'
    # #)

    # #response = request.execute()

    # response = spotify_api.search_for_item("artist", "Micheal Jackson", 5) 
    # names_and_ids = []
    # print(json.dumps(response, indent=4))
    # names_and_ids = list(map(lambda x: {"name": x['name'], "id": x['id']}, response))
    # print(json.dumps(names_and_ids, indent=4))

    # response = spotify_api.get_artist_top_tracks(names_and_ids[0]['id'])
    # track_names_and_ids = list(map(lambda x: {"name": x['name'], "id": x['id'], "popularity": x['popularity']}, response['tracks']))
    # print(json.dumps(track_names_and_ids, indent=4))

    # response = google_api.search_for_video(f'{track_names_and_ids[0]['name']} {names_and_ids[0]['name']}', 5, 'viewCount')

    # video_ids_and_titles = list(map(lambda x: { 'videoId': x['id']['videoId'], 'name': x['snippet']['title']}, response['items']))

    # print(json.dumps(video_ids_and_titles, indent=4))

    # # for video in video_ids_and_titles:
    # #     response = google_api.get_video_statistics(video['videoId'])
    # #     print(json.dumps(response, indent=4))
    # #     video['statistics'] = response['items'][0]['statistics']



    # # print(json.dumps(video_ids_and_titles, indent=4))

    # video = video_ids_and_titles[0]
    # response = google_api.get_video_statistics(video['videoId'])
    # video['statistics'] = response['items'][0]['statistics']
    # print(json.dumps(video, indent=4))

    # video


    # PROGRAM STARTS HERE

    # Load the data from the data sources into the database
    # data = get_data()

    #Printing the data retrieved from the data sources
    # print("Tracks")
    # print(json.dumps(data['tracks'], indent=4))
    # print("Artists")
    # print(json.dumps(data['artists'], indent=4))
    # print("Albums")
    # print(json.dumps(data['albums'], indent=4))

    # Print out stats for the data
    process_data_from_db() #(data)



    #spotify_api.search_for_item("artist","eminem", 5)
    logging.root.setLevel(logging.NOTSET)
    logging.info("Starting Python FLask")
    # load the spotify api
    app.run(debug=True)

if __name__ == '__main__':
    main()