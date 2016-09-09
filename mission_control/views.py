from flask import request, session, g, redirect, url_for, \
    render_template, flash, abort

from mission_control import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cursor = g.db.execute('select useremail,password from users')
        users = dict(cursor.fetchall())

        useremail = request.form['useremail']
        password = request.form['password']

        if useremail not in users.keys():
            flash({
                'type': 'danger',
                'title': "Invalid email.",
                'content': "We couldn't find an account with that email."
            })
        elif password != users[useremail]:
            flash({
                'type': 'danger',
                'title': "Invalid password.",
                'content': "Please check your password."
            })
        else:
            session['logged_in'] = True
            c = g.db.execute('''
                select name, acctype from users where useremail=?
                ''', (useremail,))
            username, acctype = list(c.fetchone())
            session['username'] = username
            session['acctype'] = acctype
            flash({
                'type': 'success',
                'title': "Yay!",
                'content': "You were logged in successfully"
            })
            return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash({
        'content': 'You were logged out',
        'type': 'info'
    })
    return redirect(url_for('index'))


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/dashboard/view/')
def view_scores():
    return render_template('view_scores.html')


@app.route('/dashboard/edit/')
def add_scores():
    return render_template('add_scores.html')


@app.route('/settings/')
def settings():
    return render_template('settings.html')


# Static pages
@app.route('/help/')
def help():
    return render_template('help.html')
