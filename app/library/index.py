from app.requests.request import home_setup, autocomplete_search, search_by_id;
from flask import Blueprint, render_template, session, request, jsonify;
# ---------------------------------------------------------------------------------------------------- #
_index = Blueprint("_index", __name__, url_prefix="/")

@_index.route("/")
def index():
    setup()
    return render_template(
        "index.html", 
        genres = session['genres'], 
        tags = session['tags'], 
        platforms = session['platforms']
    )
# ---------------------------------------------------------------------------------------------------- #   
@_index.route("/game_search", methods=["POST"])
def game_search():
    genre = request.form['genre']
    tag = request.form['tag']
    platform = request.form['platform']
    print(f"Genre: {genre} | Tag: {tag} | Platform: {platform}")
    
    return index()

@_index.route("/game_autocomplete")
def game_autocomplete():
    return autocomplete_search(request.args.get('term', '')) # jQuery UI sends 'term' by default

@_index.route('/fetch_game_details', methods=["GET"])
def fetch_game_details():
    ids = request.args.getlist("id")
    if ids: return search_by_id(ids)
    else: return jsonify({"error": "Game IDs required!"}), 400
# ---------------------------------------------------------------------------------------------------- #
def setup():
    genres, tags, platforms = home_setup()
    
    if genres is not None: session['genres'] = genres
    if tags is not None: session['tags'] = tags 
    if platforms is not None: session['platforms'] = platforms
# ---------------------------------------------------------------------------------------------------- #