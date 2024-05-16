import requests, json, logging
from flask import Blueprint, render_template, redirect, url_for, request, session
# ---------------------------------------------------------------------------------------------------- #
_login = Blueprint("_login", __name__, url_prefix="/login")

@_login.route("/")
def login():
    session.clear()
    return render_template("login.html")
# ---------------------------------------------------------------------------------------------------- #
@_login.route("/process", methods=["POST"])
def process():
    user_id = request.form.get("id", None)
    password = request.form.get("pass", None)
    
    if user_id is None or password is None:
        return redirect(url_for("_login.login", error = "Enter Both Fields"))
    
    fetch = fetch_user(user_id, password)
    
    if fetch is None:
        session["user"] = user_id
        return redirect(url_for("_index.index"))
    else:
        return redirect(url_for("_login.login", error = fetch))
# ---------------------------------------------------------------------------------------------------- #
def fetch_user(user_id, password):
    url = "https://pkxwtya6si.execute-api.us-east-1.amazonaws.com/prod/user_find"
    headers = { 'Content-Type': 'application/json' }
    payload = { "userID": user_id, "password": password }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200: 
            logging.info("Success! User Found")
            return None
        else: 
            logging.error(f"Insert Error: {response.status_code} - {response.text}")
            return response.text.replace("\"", "")
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP Request Error: {e}")
        return "An Error Has Occured! Please Try Again"
# ---------------------------------------------------------------------------------------------------- #