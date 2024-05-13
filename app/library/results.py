from app.requests.request import home_setup;
from flask import Blueprint, render_template, session;
# ---------------------------------------------------------------------------------------------------- #
_results = Blueprint("_results", __name__, url_prefix="/your-results")

@_results.route("/")
def results():
    return render_template("results.html", games = session["results"])
# ---------------------------------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------------------------------- #