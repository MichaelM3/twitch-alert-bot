from flask import Flask
from methods import twitch

app = Flask(__name__)

@app.route("/")
def hello_world():
    access_token = twitch.get_access_token()
    got_token = False
    if access_token:
        got_token = True
    return f"<h1>Got token: {got_token}</h1>"
