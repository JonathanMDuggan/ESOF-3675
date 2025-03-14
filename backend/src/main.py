import os
from example_func import OutlierExample, popularity_example, duration_distribution_example, box_plot, correlation, correlation_youtube
from data_collect import get_data, process_data_from_db
from youtube_func import GoogleAPIFacade
from spotify_func import SpotifyAPIFacade
from flask import Flask, render_template, request, jsonify
import logging
import pandas
import requests 
import json
import matplotlib.pyplot as plt
import pandas as pd
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<home>')
def name():
    return 'You typed home in the funny thing <home>'

def main():
    yt = GoogleAPIFacade("YOUTUBE_API_KEY")
    #canada_charts = yt.get_ytmusic().get_charts('CA')

    #url = 'https://charts.youtube.com/youtubei/v1/browse?alt=json'
#
    #data = {"context":{"client":{"clientName":"WEB_MUSIC_ANALYTICS","clientVersion":"2.0","hl":"en","gl":"CA","experimentIds":[],"experimentsToken":"","theme":"MUSIC"},"capabilities":{},"request":{"internalExperimentFlags":[]}},"browseId":"FEmusic_analytics_charts_home","query":"perspective=CHART_DETAILS&chart_params_country_code=au&chart_params_chart_type=TRACKS&chart_params_period_type=WEEKLY"}
#
    #response = requests.post(url, json=data)
#
    #tracks_data = None
    ## Check if the request was successful (status cde 200)
    #if response.status_code == 200:
    #    tracks_data = response.json()
    #else:
    #    print('Error:', response.status_code)
    #
    #print(json.dumps(tracks_data, indent=4))

    # print(json.dumps(str(canada_charts), indent=4))
    # OutlierExample()
    correlation_youtube()
    #logging.root.setLevel(logging.NOTSET)
    #logging.info("Starting Python FLask")
    #app.run(debug=True)

if __name__ == '__main__':
    main()