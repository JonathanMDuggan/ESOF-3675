import requests
from bs4 import BeautifulSoup

from mongo_func import MongoDBFacade

def get_genres():
    url = "https://everynoise.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    genres = []
    for genre in soup.find_all('div', class_='genre'):
        genres.append(genre.text)
    return genres


def load_and_get_genres_into_db(mongodbClient: MongoDBFacade, database_name, collection_name):
    existing_database = mongodbClient.get_database(database_name)
    if existing_database.get_collection(collection_name) == None:
        mongodbClient.create_collection(database_name, collection_name)
    existing_genres = mongodbClient.find_many(database_name, collection_name, {})
    existing_genres = list(existing_genres)
    if len(existing_genres) > 0:
        ## return dictionary of genres with a key of genre_name
        return dict([(genre['genre_name'], genre["_id"]) for genre in existing_genres])
    genres = get_genres()
    mongodbClient.insert_many(database_name, collection_name, [{"genre_name": genre.strip('» ')} for genre in genres])
    existing_genres = mongodbClient.find_many(database_name, collection_name, {})
    existing_genres = list(existing_genres)
    return dict([(genre['genre_name'], genre["_id"]) for genre in existing_genres])