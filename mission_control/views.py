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
            session['email'] = useremail
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
    session.pop('email', None)
    flash({
        'content': 'You were logged out.',
        'type': 'info'
    })
    return redirect(url_for('index'))


# These are only accessible when the user is logged in.
# a 403 is returned when someone else tries to access this.
# THIS WILL BREAK THE OLDER TESTS!
#
# We can create a custom 403 later. This will nicely ask the users to login.
# + a 404 for all those lost wanderers.

@app.route('/dashboard/')
def dashboard():
    if session['logged_in']:
        return render_template('dashboard.html')
    return abort(403)


@app.route('/dashboard/view/')
def view_scores():
    if session['logged_in']:
        # a student is directly led to their view score page.
        if session['acctype'] == 'STU':
            cursor = g.db.execute('''
                select scoreC1,scoreC2,scoreC3,scoreC4 
                    from scores where studentemail=?
                ''', (session['email'],))
            scores = list(cursor.fetchone())
            return render_template('view_scores.html',
                                   scores=zip(range(len(scores)), scores))
        # a faculty memeber is led to a page listing all the students.
        if session['acctype'] == 'FAC':
            cursor = g.db.execute('''
                select useremail,name from users where acctype='STU'
                ''')
            studentlist = [{
                'name': s_name,
                'email': s_email,
                'link': s_email.split('@')[0]
                } for s_email, s_name in list(cursor.fetchall())]
            return render_template('view_scores.html',
                                    studentlist=studentlist)
    return abort(403)


@app.route('/dashboard/view/<student>/')
def view_student_score(student):
    if session['logged_in']:
        # a faculty can view pretty much everyones scores, so just let them
        # view the required page
        if (session['acctype'] == 'FAC'):
            cursor = g.db.execute('''
                select scoreC1,scoreC2,scoreC3,scoreC4 
                    from scores where studentemail=?
                ''', ('{}@muwci.net'.format(student),))
            scores = list(cursor.fetchone())
            return render_template('view_scores.html',
                                   scores=zip(range(len(scores)), scores))
        # if a student tries to access this page, we redirect them to their
        # view scores page
        if session['acctype'] == 'STU':
            return redirect('/dashboard/view/')
    return abort(403)


@app.route('/dashboard/edit/')
def edit_scores():
    # only a faculty account can add scores.
    if session['logged_in'] and session['acctype'] == 'FAC':
        return render_template('add_scores.html')
    return abort(403)


@app.route('/dashboard/students/')
def edit_students():
    # only a faculty account can add scores.
    if session['logged_in'] and session['acctype'] == 'FAC':
        return render_template('students.html')
    return abort(403)


# Route all missing features to a missing feature template
@app.route('/settings/')
@app.route('/help/')
@app.route('/dashboard/generate/')
@app.route('/dashboard/rubric/')
@app.route('/missing-feature/')
def missing_feature():
    return render_template('missing.html')
