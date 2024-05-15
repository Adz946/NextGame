from flask import Blueprint, render_template, request, json;
# ---------------------------------------------------------------------------------------------------- #
_results = Blueprint("_results", __name__, url_prefix="/your-nextgames")

@_results.route("/")
def results():
    games_json = request.args.get("games")
    games = json.loads(games_json) if games_json else {}
    return render_template("results.html", games = games)
# ---------------------------------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------------------------------- #