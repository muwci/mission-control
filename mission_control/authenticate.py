from flask import g

def site_login(email, password):
    """
    Tries to login the user with the given credentials to the website.

    Returns: (login_status, login_error)
        - login_status (bool)
            True for a successful login, False otherwise.
        - login_error (dict)
            Is None for a successful login and has the following
            structure for an unsuccessful login:
            * login_error['type']: one of 'danger', 'warning', 'info'
            * login_error['title']: Error title
            * login_error['content']: Possible error resolution message.
    """
    login_error = None
    login_status = False

    cursor = g.db.execute("SELECT email,password FROM users")
    users = dict(cursor.fetchall())

    if email not in users.keys():
        login_error = {
            'type': 'danger',
            'title': "Invalid email.",
            'content': "We couldn't find an account with that email."
        }
    elif password != users[email]:
        login_error = {
            'type': 'danger',
            'title': "Invalid password.",
            'content': "Please check your password."
        }
    else:
        login_status = True

    return login_status, login_error

