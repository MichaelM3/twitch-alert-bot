from flask import Flask
from methods import twitch
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    params = { "login": "unbalanced_94" }

    res = requests.get(url="https://api.twitch.tv/helix/users", headers=twitch.get_headers(), params=params)
    res_json = res.json()
    return f"<h1>The user id for Unbalanced_94 is: {res_json['data'][0]['id']}</h1>"
