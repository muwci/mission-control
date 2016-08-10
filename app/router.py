from flask import render_template
from flask import request

from app import app
from app.cred_manager.auth import authenticate_login

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login_router():
    if request.method == 'POST':
        if authenticate_login(request.form['username'], password=None):
            return render_template("dashboard.html", title="Dashboard")
        else:
            error = "Login Failed! Please check login credentials."
            return render_template("login.html", title="Login", error=error)
    else:
        return render_template("login.html", title="Login")

@app.route('/about')
def about():
    return render_template("about.html", title="About")
