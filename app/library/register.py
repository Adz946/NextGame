from flask import Blueprint, render_template
# ---------------------------------------------------------------------------------------------------- #
_register = Blueprint("_register", __name__, url_prefix="/register")

@_register.route("/")
def register():
    return render_template("register.html")
# ---------------------------------------------------------------------------------------------------- #
@_register.route("/process")
def process():
    print("Stuff")
    return register()
# ---------------------------------------------------------------------------------------------------- #