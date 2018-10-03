from flask import Flask
from app.library import library_mod


def create_app():
    app = Flask(__name__)
    app.register_blueprint(library_mod, url_prefix="/library")
    return app
