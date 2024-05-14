import app.requests.request as query;
from flask import Blueprint, render_template, redirect, url_for, session, request, json, jsonify;
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
    genres = request.form['similar_genres']
    tags = request.form['similar_tags']
    platforms = request.form['similar_platforms']
    limit = request.form['search_limit']
    
    results = query.search_for_results(genres, tags, platforms, limit)
    if results: return redirect(url_for('_results.results', games = json.dumps(results)))
    else: 
        print("Nothing Found?!")
        return index()

@_index.route("/game_autocomplete")
def game_autocomplete():
    return query.autocomplete_search(request.args.get('term', '')) # jQuery UI sends 'term' by default

@_index.route('/fetch_game_details', methods=["GET"])
def fetch_game_details():
    game_ids = request.args.getlist('ids')
    genre = request.args.get('genre').split("|")
    tag = request.args.get('tag').split("|")
    platform = request.args.get('platform').split("|")

    if game_ids: 
        return query.search_by_id(game_ids, genre[0], int(genre[1]), tag[0], int(tag[1]), platform[0], int(platform[1]))
    else: return jsonify({"error": "Game IDs required"}), 400
# ---------------------------------------------------------------------------------------------------- #
def setup():
    genres, tags, platforms = query.home_setup()
    
    if genres is not None: session['genres'] = genres
    if tags is not None: session['tags'] = tags 
    if platforms is not None: session['platforms'] = platforms
# ---------------------------------------------------------------------------------------------------- #