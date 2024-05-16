from flask import Flask;
from app.library import index, results, login, register, searches;

def setup():
    app = Flask(__name__)
    app.secret_key = "ABC123DEF456GHI789" # Hard-Coded For Simplicity

    app.register_blueprint(index._index)
    app.register_blueprint(login._login)
    app.register_blueprint(results._results)
    app.register_blueprint(register._register)
    app.register_blueprint(searches._searches)
    return app