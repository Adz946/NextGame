from app.requests.request import home_setup;
from flask import Blueprint, render_template, session;
# ---------------------------------------------------------------------------------------------------- #
_results = Blueprint("_results", __name__, url_prefix="/results")

@_results.route("/")
def index():
    setup()
    return render_template(
        "index.html", 
        genres = session['genres'], 
        tags = session['tags'], 
        platforms = session['platforms']
    )
# ---------------------------------------------------------------------------------------------------- #
def setup():
    genres, tags, platforms = home_setup()
    
    if genres is not None: session['genres'] = genres
    if tags is not None: session['tags'] = tags 
    if platforms is not None: session['platforms'] = platforms
# ---------------------------------------------------------------------------------------------------- #