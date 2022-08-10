from dotenv import load_dotenv
import os
import hmac
import hashlib
import requests
import json
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
twitch_eventsub_secret = os.getenv("TWITCH_EVENTSUB_SECRET", "")

# The Base URL for all things Event Sub
eventsub_subscription_url = "https://api.twitch.tv/helix/eventsub/subscriptions"

def get_access_token():
    access_token = os.getenv("TWITCH_ACCESS_TOKEN")
    if access_token:
        return access_token
    return generate_access_token()
    
def generate_access_token():
    # Generate an access token for authenticating requests
    auth_body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    auth_res = requests.post("https://id.twitch.tv/oauth2/token", auth_body)

    # Setup Headers for future requests
    auth_res_json = auth_res.json()

    # Set environment variable
    os.environ["TWITCH_ACCESS_TOKEN"] = auth_res_json["access_token"]
    return os.getenv("TWITCH_ACCESS_TOKEN")

def get_headers():
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {get_access_token()}"
    }
    return headers

def validate_access_token(token):
    validate_headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        res = requests.get(url="https://id.twitch.tv/oauth2/validate", headers=validate_headers)
        res_json = res.json()
        return res.status_code == requests.codes.ok and res_json["client_id"] == client_id
    except:
        return False

def verify_signature(req):
    hmac_message = req.headers['Twitch-Eventsub-Message-Id'] + req.headers['Twitch-Eventsub-Message-Timestamp'] + req.data.decode()
    message_signature = "sha256=" + hmac.new(str.encode(twitch_eventsub_secret), str.encode(hmac_message), hashlib.sha256).hexdigest()
    if message_signature == req.headers['Twitch-Eventsub-Message-Signature']:
        return True
    return False

