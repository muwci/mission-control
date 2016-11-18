from mission_control import app
from mission_control import socketio

import mission_control.database

socketio.run(app, debug=True, host="0.0.0.0")
