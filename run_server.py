from mission_control import app
from mission_control import socketio

import mission_control.database

mission_control.database.init_db()
socketio.run(app, debug=True)
