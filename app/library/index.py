import requests, logging
import app.requests.request as query;
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify;
# ---------------------------------------------------------------------------------------------------- #
_index = Blueprint("_index", __name__, url_prefix="/")

@_index.route("/")
def index():
    if "savedIDs" in session: session["savedIDs"] = None 
    if "gameIDs" in session: session["gameIDs"] = None  
    error = request.args.get("error")
    
    user_id = session["user"] if setup() else None
    user = get_user(user_id)
    
    return render_template(
        "index.html", 
        genres = session.get("genres"), 
        tags = session.get("tags"), 
        platforms = session.get("platforms"), 
        user = user,
        error = error
    )
# ---------------------------------------------------------------------------------------------------- #
def setup():
    if "genres" not in session or "tags" not in session or "platforms" not in session:
        genres, tags, platforms = query.home_setup()
        
        if genres: session["genres"] = genres
        if tags: session["tags"] = tags
        if platforms: session["platforms"] = platforms
        
    return "user" in session

def get_user(id):
    if id is not None:
        url = f"https://pkxwtya6si.execute-api.us-east-1.amazonaws.com/prod/get_user?userID={id}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200: return response.json()
            else: logging.error(f"Fetch Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e: logging.error(f"HTTP Request Error: {e}")
    
    return None
# ---------------------------------------------------------------------------------------------------- #   
@_index.route("/game_search", methods=["POST"])
def game_search():
    genres = request.form['similar_genres']
    tags = request.form['similar_tags']
    platforms = request.form['similar_platforms']
    limit = request.form['search_limit']
    
    results = query.search_for_results(genres, tags, platforms, limit)
    if results: 
        session["gameIDs"] = results
        return redirect(url_for('_results.results'))
    else: 
        return redirect(url_for('_index.index', error = "No Games Found"))
# ---------------------------------------------------------------------------------------------------- #
@_index.route("/game_autocomplete")
def game_autocomplete():
    return query.autocomplete_search(request.args.get('term', '')) # jQuery UI sends 'term' by default
# ---------------------------------------------------------------------------------------------------- #
@_index.route('/fetch_game_details', methods=["GET"])
def fetch_game_details():
    game_ids = request.args.getlist('ids')
    genre = request.args.get('genre').split("|")
    tag = request.args.get('tag').split("|")
    platform = request.args.get('platform').split("|")

    if game_ids: 
        return query.search_by_id(game_ids, genre[0], int(genre[1]), tag[0], int(tag[1]), platform[0], int(platform[1]))
    else: 
        return jsonify({"error": "Game IDs required"}), 400
# ---------------------------------------------------------------------------------------------------- #