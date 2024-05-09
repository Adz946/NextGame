from flask import Flask;
from app.library import index;

def setup():
    app = Flask(__name__)
    app.secret_key = "ABC123DEF456GHI789" # Hard-Coded For Simplicity

    app.register_blueprint(index._index)
    return app