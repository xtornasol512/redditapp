import os
import urllib
from uuid import uuid4
import requests
from flask import Flask, render_template, abort, request

# Reddit Config
CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]
CLIENT_SECRET = os.environ["REDDIT_CLIENT_SECRET"]
REDIRECT_URI = "https://{}.herokuapp.com/{}".format(
    os.environ["HEROKU_APP_NAME"],
    os.environ["REDDIT_REDIRECT_URI"]
    )

app = Flask(__name__)

@app.route("/")
def hello():
    url_auth = make_authorization_url()
    return render_template("home.html", url_auth=url_auth)


@app.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    # We'll change this next line in just a moment
    return "got a code! %s" % get_token(code)


def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    state = str(uuid4())
    save_created_state(state)
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "state": state,
        "redirect_uri": REDIRECT_URI,
        "duration": "temporary",
        "scope": "identity"
    }
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.urlencode(params)
    return url

# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
    pass

def is_valid_state(state):
    return True

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(
        "https://ssl.reddit.com/api/v1/access_token",
        auth=client_auth,
        data=post_data
    )
    token_json = response.json()
    print(token_json)
    return token_json["access_token"]
