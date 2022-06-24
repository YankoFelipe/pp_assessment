import os
import re
import json
from typing import Dict, List, Tuple

from flask import Flask, g
from flask import request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import db
from entities.plate import Plate
from repositories import plate_repo


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
        ap = db.session.query(Plate).all()
        print(ap)


app = create_app()


@app.before_request
def before_request():
    engine = create_engine('sqlite:////tmp/test.db', echo=True)
    Base = declarative_base()
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    g.session = Session()
    print('new session: ', g.session)


@app.route("/")
def hello_world():
    return "<p>Peter Park assessment by Yanko Arévalo</p>"


@app.route('/plate', methods=['GET', 'POST'])
def plate():
    if request.method == 'POST':
        print('post')
        print(request.__dict__)
        print(request.form)
        try:
            a = request.json
        except Exception as e:
            print(e)
        return post_plate(request.json)
    else:
        return get_plate()


@app.route('/search-plate', methods=['GET'])
def search_plate():
    key = args.get("key")
    if not isinstance(key, str):
        return 422, "Missing key to search"
    # Unhypening... just in case
    key = key.replace("-", "")
    levenshtein = args.get("levenshtein")
    if not isinstance(levenshtein, str) or not levenshtein.isnumeric():
        return 422, "Invalid levenshtein, must be a number"
    levenshtein = int(levenshtein)
    all_plates = plate_repo.get_all()
    is_close = lambda x: x.levenshtein_distance(key) <= levenshtein
    return [plate.serialize() for plate in map(is_close, all_plates)]


def post_plate(plate_data: Dict) -> Tuple[str, int]:
    plate = plate_data.get("plate", None)
    if plate is None:
        return "Malformed request, it must contain the key 'plate'", 400
    if not is_valid_plate(plate):
        return "Key 'plate' must be a valid german plate", 422
    return plate_repo.save()


def get_plate() -> str:
    serialized_plates = [p.serialize() for p in plate_repo.get_all()]
    return json.dumps(serialized_plates)


def is_valid_plate(plate: str) -> bool:
    print('validating')
    if not isinstance(plate, str):
        return False
    by_hypen = plate.split('-')
    if len(by_hypen) != 2:
        return False
    if len(by_hypen[0]) == 0 or len(by_hypen[0]) > 3:
        return False
    split_post_hypen = re.split(r'(\d+|\s+)', by_hypen[1])
    if not isinstance(split_post_hypen, list) or len(split_post_hypen) != 3:
        return False
    if len(split_post_hypen[0]) not in [1, 2]:
        return False
    if len(split_post_hypen[1]) > 4 or split_post_hypen[1][0] == '0':
        return False
    return True


if __name__ == '__main__':
    setup_database(app)
    app.run()

# def test_login():
#   payload = {"ecosystem":'abc'}
#   accept_json=[('Content-Type', 'application/json;')]
#   response = client.post('/data_extraction'), data=json.dumps(payload), headers=accept_json)
#   assert response.data == {'foo': 'bar'}
