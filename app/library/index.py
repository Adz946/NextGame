from app.requests.request import search_dataset, search_by_id;
from flask import Blueprint, render_template, session;
# ---------------------------------------------------------------------------------------------------- #
_index = Blueprint("_index", __name__, url_prefix="/")

@_index.route("/")
def index():
    setup()
    return render_template(
        "index.html", 
        genres = session['genres'], 
        tags = session['tags'], 
        platforms = session['platforms'],
        game = session["game"]
    )
# ---------------------------------------------------------------------------------------------------- #
def setup():
    if 'genres' not in session:
        genres = search_dataset(url_end = "genres")
        if genres is not None:  session['genres'] = genres
    
    if 'tags' not in session:
        tags = search_dataset(url_end = "tags")
        if tags is not None: session['tags'] = tags
    
    if 'platforms' not in session:
        platforms = search_dataset(url_end = "platforms")
        if platforms is not None: session['platforms'] = platforms
        
    if 'game' not in session:
        game = search_by_id(13536)
        if game is not None: session["game"] = game
# ---------------------------------------------------------------------------------------------------- #