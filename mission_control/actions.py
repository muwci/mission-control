from flask import flash
from flask import g
from flask import session

from rubric.convertor import rubric_name_map
from rubric.convertor import struct
from rubric.utils import fill_tree


def login(email):
    """
    Sets session variables, flashes a 'Login successful' message for the
    given email id.

    Returns: None
    """
    c = g.db.execute("""
        SELECT name, username, acctype
        FROM users
        WHERE email=?
    """, (email,))
    name, username, acctype = list(c.fetchone())

    session['logged_in'] = True
    session['name'] = name
    session['username'] = username
    session['email'] = email
    session['acctype'] = acctype

    flash({
        'type': 'success',
        'content': "You were logged in successfully"
    })


def logout():
    """
    Unsets the session variables and flashes a 'Logout successful'
    message.

    Returns: None
    """
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('name', None)
    session.pop('email', None)

    flash({
        'type': 'info',
        'content': 'You were logged out.'
    })


def get_student_dashboard_data():
    return None


def get_faculty_dashboard_data():
    """
    Returns: data (dict)
        data used by the faculty dashboard template.
    """
    c = g.db.execute("SELECT year FROM students")
    years = set([year for (year,) in c.fetchall()])

    c = g.db.execute("""
        SELECT users.username,users.name,users.email,students.year
        FROM users
        INNER JOIN students
        ON students.username=users.username
        WHERE users.acctype='STU'
    """)
    students = {
        username: {
            'name': name,
            'email': email,
            'year': year
        }
        for username, name, email, year in c.fetchall()
    }

    classes = {
        year: [user for user in students if students[user]['year'] == year]
                        for year in years
    }

    data = {'classes': classes, 'students': students}
    return data


def score_viewer_data(student):
    """
    Returns: data (dict)
        dictionary with all the values required to view the student
        score using the view_scores.html template.
    """
    data = {
        'rubric_headers': get_rubric_headers(),
        'graph': struct.node_dict,
        'scores': get_all_student_scores(student),
        'name_map': rubric_name_map,
        'student': student
    }
    return data


def get_student_scores(student, term=1):
    """
    Returns: (criteria, score) pairs (list of tuples)
        list of (criteria, score) tuples for the given student.
    """
    c = g.db.execute("""
        SELECT *
        FROM grades
        WHERE username=? AND term=?
    """, (student, term))

    scores = list(c.fetchone())
    return zip(list(sorted(rubric_name_map.keys())), scores[2:])


def get_all_student_scores(student):
    """
    Returns: {criteria:{term:score}} (dict)
        Dictionary of criteria:scores pairs for the given student.
        Each value in the dictionary will be a dictionary with the
        term as key and the score as value.
    """

    all_scores = {ky:{} for ky in rubric_name_map.keys()}

    c = g.db.execute("""
        SELECT term
        FROM grades
        WHERE username=?
    """, (student,))

    terms = list(c.fetchall())

    for (term,) in terms:
        c = g.db.execute("""
            SELECT *
            FROM grades
            WHERE username=? AND term=?
        """, (student, term))
        term_scores = list(c.fetchone())[2:]
        for criteria, score in zip(sorted(all_scores.keys()), term_scores):
            all_scores[criteria][term] = score
    return all_scores

def get_rubric_headers():
    """
    Returns: list of rubric roots (list)
    """
    return [c for c in sorted(rubric_name_map.keys()) if len(c) == 1]


def update_scores(form_input, student, term):
    """
    From the given form input, updates the scores in the database for
    the given student and term.

    Returns:
        None
    """
    input_tree = form_input.copy()
    filled_tree = fill_tree(input_tree)
    setter_string = ', '.join(["%s=%s" % (ky, filled_tree[ky])
                                          for ky in filled_tree])

    db_query = """
        UPDATE grades
        SET %s
        WHERE username='%s' AND term=%s
    """ % (setter_string, student, term)

    cursor = g.db.execute(db_query)
    g.db.commit()

    return None
