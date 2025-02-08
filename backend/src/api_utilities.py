import os
import json
import logging
import base64
from requests import post
# Load the api from the .env file
def load_api(API_CLIENT_ID_NAME: str, API_CLIENT_SECERT_NAME: str, URL: str):
    CLIENT_ID     = os.getenv(API_CLIENT_ID_NAME)
    CLIENT_SECERT = os.getenv(API_CLIENT_SECERT_NAME)

    if CLIENT_ID == None or CLIENT_SECERT == None:
        logging.error("%s is: %s", API_CLIENT_ID_NAME, CLIENT_ID)
        logging.error("%s is: %s", API_CLIENT_SECERT_NAME, CLIENT_SECERT)
        return None
    else:
        logging.info("Successfully loaded %s and %s", API_CLIENT_ID_NAME, API_CLIENT_SECERT_NAME)

    AUTH_STRING = CLIENT_ID + ":" + CLIENT_SECERT
    AUTH_BYTES = AUTH_STRING.encode("utf-8")
    AUTH_BYTES64 = str(base64.b64encode(AUTH_BYTES), "utf-8")

    headers = {
        "Authorization": "Basic " + AUTH_BYTES64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(URL, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token
