from flask import Blueprint, render_template
# ---------------------------------------------------------------------------------------------------- #
_login = Blueprint("_login", __name__, url_prefix="/login")

@_login.route("/")
def login():
    return render_template("login.html")
# ---------------------------------------------------------------------------------------------------- #
@_login.route("/process")
def process():
    print("Stuff")
    return login()
# ---------------------------------------------------------------------------------------------------- #