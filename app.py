import os
from flask import Flask, render_template

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
    return render_template("home.html")