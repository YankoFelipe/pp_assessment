import os

from flask import Flask

from db import db
# TODO: REMOVE THIS
from entities.plate import Plate


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
    db.init_app(app)
    return app


def setup_database(app):
    # TODO: Remove this once db is tested
    if os.path.isfile('/tmp/test.db'):
        os.remove('/tmp/test.db')
    with app.app_context():
        db.create_all()
        plate = Plate('as-a123')
        db.session.add(plate)
        db.session.commit()
