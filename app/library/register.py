import requests, json, logging, bcrypt, base64
from flask import Blueprint, render_template, redirect, url_for, request, session
# ---------------------------------------------------------------------------------------------------- #
_register = Blueprint("_register", __name__, url_prefix="/register")

@_register.route("/")
def register():
    error = request.args.get("error")
    return render_template("register.html", error = error)
# ---------------------------------------------------------------------------------------------------- #
@_register.route("/process", methods=['POST'])
def process():
    data = [
        request.form.get(item, None) for item in 
        ["id", "name", "pass", "v_pass", "f_name", "m_name", "l_name", "email", "mobile", "street", "city", "state", "postal"]
    ]
    profile = request.files.get("profile_img", None)
    
    if data[2] == data[3]:
        logging.info("Password Match! Sending to DB")
        hashed = bcrypt.hashpw(data[2].encode('utf-8'), bcrypt.gensalt())
        password = hashed.decode("utf-8")
        address = f"{data[9]}, {data[10]} {data[11]}, {data[12]}"
        user = [data[0], data[1], password, data[4], data[5], data[6], data[7], data[8], address]
    else:
        logging.info("Passwords Do Not Match! Returning to Register Page")
        return redirect(url_for("_register.register", error = "Passwords Do Not Match"))
    
    image = base64.b64encode(profile.read()).decode('utf-8') if profile else None
    insert = insert_user(user, image)
    
    if insert is None:
        session["user"] = user[0]
        return redirect(url_for("_index.index"))
    else:
        return redirect(url_for("_register.register", error = insert))
# ---------------------------------------------------------------------------------------------------- #
def insert_user(user, image):
    url = "https://pkxwtya6si.execute-api.us-east-1.amazonaws.com/prod/user_insert"
    headers = { 'Content-Type': 'application/json' }
    payload = { "user": user, "image": image }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200: 
            logging.info("Success! User Added To DB [+ Image to S3]")
            return None
        else: 
            logging.error(f"Insert Error: {response.status_code} - {response.text}")
            return response.text.replace("\"", "")
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP Request Error: {e}")
        return "An Error Has Occured! Please Try Again"
# ---------------------------------------------------------------------------------------------------- #