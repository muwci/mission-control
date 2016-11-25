import sqlite3
from contextlib import closing
from flask import g

from mission_control import app


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('reset.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        with app.open_resource('populate.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    # print('Initialized database.')


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
