from flask import flash
from flask import g
from flask import session

from rubric.convertor import name_map

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
        year:[user for user in students if students[user]['year'] == year]
            for year in years
    }

    data = {'classes':classes, 'students':students}
    return data


def get_student_scores(student):
    """
    Returns: scores (dict)
        dictionary of criteria:score pairs for the given student.
    """
    c = g.db.execute("""
        SELECT *
        FROM grades
        WHERE username=?
        """, (student,))
    
    scores = list(c.fetchone())
    return zip(list(sorted(name_map.keys())), scores[1:])
