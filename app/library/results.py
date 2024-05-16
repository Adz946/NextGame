import requests, json, logging
from app.requests.request import get_game_results
from flask import Blueprint, render_template, redirect, url_for, request, json, session;
# ---------------------------------------------------------------------------------------------------- #
_results = Blueprint("_results", __name__, url_prefix="/your-nextgames")

@_results.route("/")
def results():
    user_id = session["user"] if "user" in session else None
    user = get_user(user_id)
    
    game_ids = session["gameIDs"] if "gameIDs" in session else None
    games = get_game_results(game_ids)
    
    saved = session['savedIDs'] if "savedIDs" in session else None
    
    return render_template("results.html", saved = saved, game_ids = game_ids, games = games, user = user)
# ---------------------------------------------------------------------------------------------------- #
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
@_results.route("/save_game_ids", methods=['POST'])
def save_game_ids():
    game_ids = request.form.get("game_ids", None)
    print(f"Game IDs: {game_ids}")
    
    if game_ids:
        logging.info(f"Game IDs: {game_ids}")
        save = save_to_db(game_ids)
        session['savedIDs'] = save
    else:
        logging.info("Nothing FOUND")
        
    return redirect(url_for("_results.results"))
# ---------------------------------------------------------------------------------------------------- #
def save_to_db(game_ids):
    url = "https://pkxwtya6si.execute-api.us-east-1.amazonaws.com/prod/search_insert"
    headers = { 'Content-Type': 'application/json' }
    payload = { "userID": session["user"], "gameIDs": game_ids }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200: 
            logging.info(f"IDs Saved for User [{session["user"]}] | {[game_ids]}")
            return True
        else:
            logging.error(f"Insert Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP Request Error: {e}")
    
    return False
# ---------------------------------------------------------------------------------------------------- #