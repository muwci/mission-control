from flask import abort
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from mission_control import actions
from mission_control import app
from mission_control import authenticate

from rubric.convertor import struct
from rubric.convertor import rubric_name_map
from rubric.utils import fill_tree


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Tries to perform login on a POST request. Returns a redirect to the
    dashboard on a successful login and displays the home page with the
    login error message otherwise.

    Returns the home page on all other request methods.
    """

    if request.method == 'POST':

        email = request.form['useremail']
        password = request.form['password']
        login_success, login_error = authenticate.site_login(email, password)

        if login_success:
            actions.login(email)
            return redirect('/dashboard/')
        else:
            return render_template('index.html', error=login_error)

    return render_template('index.html', title='Home')


@app.route('/logout/')
def logout():
    """
    Logs out the user.

    returns: a redirect to the home page.
    """
    actions.logout()
    return redirect('/')


@app.route('/dashboard/')
def dashboard():
    """
    returns:
        The appropriate dashboard based on the account type if the user
        is logged in. A 403 abort is returned otherwise.
    """
    if session['logged_in']:
        if session['acctype'] == 'STU':
            return render_template('dashboard_stu.html',
                                   data=actions.get_student_dashboard_data(),
                                   title="Dashboard")
        elif session['acctype'] == 'FAC':
            return render_template('dashboard_fac.html',
                                   data=actions.get_faculty_dashboard_data(),
                                   title="Dashboard")
    return abort(403)


@app.route('/dashboard/view/')
def view_scores():
    """
    Return the scores page if the student tries to access her scores. A
    403 abort is returned for all other cases.
    """
    if session['logged_in']:
        if session['acctype'] == 'STU':
            student = session['username']
            data = {
                'scores': actions.get_student_scores(student),
                'name_map': rubric_name_map
            }
            return render_template('view_scores.html',
                                   data=data,
                                   title="View Scores")
    return abort(403)


@app.route('/dashboard/view/<student>/')
def view_student_score(student):
    """
    Redirect the user to her own view scores page if she tries to access
    this. Faculty should be shown the scores page for the requested
    student. Return a 403 for users who are not logged in.
    """
    if session['logged_in']:
        if (session['acctype'] == 'FAC'):
            data = {
                'scores': actions.get_student_scores(student),
                'name_map': rubric_name_map
            }
            return render_template('view_scores.html',
                                   data=data,
                                   title="%s - scores" % (student,))
        elif session['acctype'] == 'STU':
            return redirect('/dashboard/view/')
    return abort(403)


@app.route('/dashboard/edit/<student>/', methods=['GET', 'POST'])
def edit_student_score(student):
    if session['logged_in'] and (session['acctype'] == 'FAC'):
        if request.method == 'GET':
            graph_map = list(sorted(struct.node_dict.keys()))
            cursor = g.db.execute('''
                select * from grades where username='{}'
                '''.format(student))
            scores = list(cursor.fetchone())[1:]
            return render_template('add_scores.html',
                                    structure=graph_map,
                                    rubric_name_map=rubric_name_map,
                                    scores=dict(zip(graph_map, scores)))
        elif request.method == 'POST':
            filled_tree = fill_tree(request.form)
            db_query = "UPDATE grades SET {} WHERE username='{}'".format(
                ', '.join(["%s=%s" % (ky, filled_tree[ky])
                    for ky in filled_tree]),
                student)
            cursor = g.db.execute(db_query)
            g.db.commit()
            flash({
                'content': "Scores updated for {}".format(student),
                'type': 'success'
            })
            return redirect('/dashboard/')
    return abort(403)


@app.errorhandler(404)
def missing_feature(e):
    return render_template('404.html', title='Not Found'), 404

@app.errorhandler(403)
def forbidden(e):
    flash({
        'type': 'danger',
        'title': "Forbidden!",
        'content': """
            You don't have privileges to access that part of the website.
            Please make sure you are logged in with the correct account.
        """
    })
    return redirect('/'), 403
