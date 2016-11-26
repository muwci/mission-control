from flask import flash
from flask import g
from flask import session

def login(email):
    """
    Sets session variables, flashes a 'Login successful' message for the
    given email id.

    Returns: None
    """
    c = g.db.execute('''
        SELECT name, acctype FROM users WHERE useremail=?
    ''', (email,))
    username, acctype = list(c.fetchone())

    session['logged_in'] = True
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
    session.pop('email', None)
    flash({
        'type': 'info',
        'content': 'You were logged out.'
    })
