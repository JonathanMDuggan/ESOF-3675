import os
from example_func import OutlierExample, popularity_example, duration_distribution_example, box_plot, correlation
from data_collect import get_data, process_data_from_db
from youtube_func import GoogleAPIFacade
from spotify_func import SpotifyAPIFacade
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap 
from views.views import views
import logging
import pandas
import requests 
import json
import matplotlib.pyplot as plt
import pandas as pd
# Flask route source code is stored in the views folder
app = Flask(__name__)
app.config['SECRET_KEY'] = "123"
bootstrap = Bootstrap(app)
app.register_blueprint(views)
def main():
    RUN_WEB_SERVER = True
    if RUN_WEB_SERVER:
        app.run(debug=True)
    else:
        process_data_from_db()

if __name__ == '__main__':
    main()