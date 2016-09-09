from mission_control import app
import mission_control.database

mission_control.database.init_db()
app.run(debug=True)
