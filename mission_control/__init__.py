from flask import Flask
from flask_socketio import SocketIO

# configuration
DATABASE = './rubric/data/mission_control.db'
DEBUG = True
SECRET_KEY = 'development key'

# flask app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

app.jinja_env.globals.update(len=len)
app.jinja_env.globals.update(sorted=sorted)

socketio = SocketIO(app, async_mode=None)

import mission_control.database
import mission_control.views

