import os
import pymongo
from api_utilities import connect_spotify_api
import logging
from dotenv import load_dotenv
from requests import get, post, exceptions


class MongoDBFacade:
    def __init__(self, CONNECTION_STRING_NAME):
        load_dotenv()
        self.CONNECTION_STRING = os.getenv(CONNECTION_STRING_NAME)
        if self.CONNECTION_STRING == None:
            logging.error("%s is: %s", CONNECTION_STRING_NAME, 
                          self.CONNECTION_STRING)
            return None
        else:
            logging.info("Successfully loaded %s and %s", 
                        CONNECTION_STRING_NAME, self.CONNECTION_STRING)
        self.client = pymongo.MongoClient(self.CONNECTION_STRING)
        return
    
    def create_database(self, database_name):
        return self.client[database_name]
    
    def create_collection(self, database_name, collection_name):
        return self.client[database_name][collection_name]
    
    def get_database(self, database_name):
        return self.client[database_name]
    
    def get_collection(self, database_name, collection_name):
        return self.client[database_name][collection_name]
    
    def insert_one(self, database_name, collection_name, document):
        self.client[database_name][collection_name].insert_one(document)
        return
    
    def insert_many(self, database_name, collection_name, documents):
        self.client[database_name][collection_name].insert_many(documents)
        return
    
    def find_one(self, database_name, collection_name, query):
        return self.client[database_name][collection_name].find_one(query)
    
    def find_many(self, database_name, collection_name, query):
        return self.client[database_name][collection_name].find(query)
    
    def update_one(self, database_name, collection_name, query, update):
        self.client[database_name][collection_name].update_one(query, update)
        return
    
    def update_many(self, database_name, collection_name, query, update):
        self.client[database_name][collection_name].update_many(query, update)
        return
    
    def delete_one(self, database_name, collection_name, query):
        self.client[database_name][collection_name].delete_one(query)
        return
    
    def delete_many(self, database_name, collection_name, query):
        self.client[database_name][collection_name].delete_many(query)
        return
    
    def drop_database(self, database_name):
        self.client.drop_database(database_name)
        return
    
    def drop_collection(self, database_name, collection_name):
        self.client[database_name].drop_collection(collection_name)
        return
    
    def list_databases(self):
        return self.client.list_database_names()
    
    def list_collections(self, database_name):
        return self.client[database_name].list_collection_names()
    
    def close(self):
        self.client.close()
        return
    
    def __del__(self):
        self.close()
        return

    