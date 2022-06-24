from flask import g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
#session = Session(engine)
#registry().metadata.create_all(engine)

#current_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy()

def get_session(app):
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base = declarative_base()
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()
