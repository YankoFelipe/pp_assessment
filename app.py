import os

from flask import g
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from repositories import plate_repo
from use_cases import get_plate, post_plate, search_plate_fn
from setup import create_app, setup_database


load_dotenv()

app = create_app()


@app.before_request
def before_request():
    engine = create_engine('sqlite:////tmp/test.db', echo=True)
    # Base = declarative_base()
    # Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    g.session = Session()
    print('new session: ', g.session)


@app.route("/")
def hello_world():
    return "<p>Peter Park assessment by Yanko Arévalo</p>"


@app.route('/plate', methods=['GET', 'POST'])
def plate():
    if request.method == 'POST':
        return post_plate(request.json, plate_repo)
    else:
        return get_plate(plate_repo)


@app.route('/search-plate', methods=['GET'])
def search_plate():
    return search_plate_fn(request.args, plate_repo)


if __name__ == '__main__':
    setup_database(app)
    app.run(port=os.getenv('FLASK_RUN_PORT'))
