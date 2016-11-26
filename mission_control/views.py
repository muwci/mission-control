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

from rubric.convertor import hierarchy
from rubric.convertor import name_map
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

    return render_template('index.html')

@app.route('/logout/')
def logout():
    """
    Logs out the user.

    returns: a redirect to the home page.
    """
    actions.logout()
    return redirect('/')


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
                select * from grades where username='{}'
                '''.format(session['email'][:-1*len('@muwci.net')]))
            scores = list(cursor.fetchone())
            return render_template('view_scores.html',
                                   scores=zip(list(sorted(name_map.keys())),
                                            scores[1:]),
                                   name_map=name_map)
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
                select * from grades where username='{}'
                '''.format(student))
            scores = list(cursor.fetchone())
            return render_template('view_scores.html',
                                   scores=zip(list(sorted(name_map.keys())),
                                            scores[1:]),
                                   name_map=name_map)
        # if a student tries to access this page, we redirect them to their
        # view scores page
        if session['acctype'] == 'STU':
            return redirect('/dashboard/view/')
    return abort(403)


@app.route('/dashboard/edit/')
def edit_scores():
    # only a faculty account can add scores.
    if session['logged_in'] and session['acctype'] == 'FAC':
        cursor = g.db.execute('''
                select useremail,name from users where acctype='STU'
                ''')
        studentlist = [{
            'name': s_name,
            'email': s_email,
            'link': s_email.split('@')[0]
            } for s_email, s_name in list(cursor.fetchall())]
        return render_template('add_scores_student_list.html',
                                studentlist=studentlist)
    return abort(403)

@app.route('/dashboard/edit/<student>/', methods=['GET', 'POST'])
def edit_student_score(student):
    if session['logged_in'] and (session['acctype'] == 'FAC'):
        if request.method == 'GET':
            graph_map = list(sorted(hierarchy.node_dict.keys()))
            cursor = g.db.execute('''
                select * from grades where username='{}'
                '''.format(student))
            scores = list(cursor.fetchone())[1:]
            # print(graph_map)
            return render_template("add_scores.html",
                                    structure=graph_map,
                                    name_map=name_map,
                                    scores=dict(zip(graph_map, scores)))
        else:
            # print(request.form)
            filled_tree = fill_tree(request.form)
            db_query = "UPDATE grades set {} WHERE username='{}'".format(
                ', '.join(["%s=%s" % (ky, filled_tree[ky])
                    for ky in filled_tree]),
                student)  
            # print(db_query)
            # query_value_string = '\'' + student + '\', ' + ', '.join([str(filled_tree[nm]) for nm in sorted(filled_tree.keys())])

            # cursor = g.db.execute('''
                # insert into grades values ({})
            # '''.format(query_value_string))
            cursor = g.db.execute(db_query)
            g.db.commit()
            flash({
                'content': "Scores updated for {}".format(student),
                'type': 'success'
            })
            return redirect('/dashboard/edit/')
    return abort(403)


@app.route('/dashboard/students/')
def edit_students():
    # only a faculty account can add scores.
    if session['logged_in'] and session['acctype'] == 'FAC':
        return render_template('students.html')
    return abort(403)


@app.errorhandler(404)
def missing_feature(e):
    return render_template('404.html'), 404

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
    return render_template('index.html'), 403
