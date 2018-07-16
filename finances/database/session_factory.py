import json
import os
from typing import Dict

from contextlib import contextmanager

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


_all_recipes = None
DB_URL = 'postgresql+psycopg2://julie:Lime204932soda@recipes-db.crls45hrmyug.us-east-1.rds.amazonaws.com:5432/recipes_db?sslmode=require'



ENGINE = None


def connect_to_db():
    engine = ENGINE
    if not engine:
        engine = create_engine(DB_URL, echo=True)
    return engine.connect()


@contextmanager
def db_session():
    engine = ENGINE
    if not engine:
        engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    try:
        session = Session()
        yield session
        session.commit()
    except:
        session.rollback()
        raise
