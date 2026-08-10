import requests
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
def token():
    resp = requests.post("https://id.twitch.tv/oauth2/token", params={
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    })

    token = resp.json()["access_token"]
    return token