from flask import Flask

from db import db
from entities.plate import Plate


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
    db.init_app(app)
    return app


def setup_database(app):
    with app.app_context():
        db.create_all()
