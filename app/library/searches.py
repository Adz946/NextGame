import requests, logging
import app.requests.request as query;
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify;
# ---------------------------------------------------------------------------------------------------- #
_searches = Blueprint("_searches", __name__, url_prefix = "/your-previous-searches")

@_searches.route("/")
def searches():
    user_id = session["user"] if "user" in session else None
    user = get_user(user_id)
    searches = get_searches(user_id)
    
    return render_template("searches.html", user = user, searches = searches)
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

def get_searches(id):
    if id is not None:
        url = f"https://pkxwtya6si.execute-api.us-east-1.amazonaws.com/prod/find_searches?userID={id}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200: return response.json()
            else: logging.error(f"Fetch Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e: logging.error(f"HTTP Request Error: {e}")
        
    return None
# ---------------------------------------------------------------------------------------------------- #
@_searches.route("/search_games", methods=["POST"])
def search_games():
    game_ids = request.form.get("game_ids", None)
    
    if game_ids:
        session["gameIDs"] = game_ids
        return redirect(url_for('_results.results'))
    
    return redirect(url_for("_searches.searches"))
# ---------------------------------------------------------------------------------------------------- #