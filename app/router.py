import csv

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from app import app


# ALL OF THIS NEEDS TO BE SENT TO ANOTHER FILE.
# THIS IS JUST HERE BECAUSE WE WANT A SIMPLE PROTOTYPE
# THIS IS BAD CODE. REALLY BAD CODE
#
# BAD CODE BEGINS HERE
#
USER_DATA_FILE = "./app/data/userlogin.csv"

user_data_reader = csv.reader(open(USER_DATA_FILE))

headers = next(user_data_reader)
user_data = {}
for username, name, account_type in user_data_reader:
    user_data[username] = {'name':name,
                            'acc':account_type,
                            'username':username}

student_scores = {username:0 for username in user_data \
                    if user_data[username]['acc'] =='STU'}

#
# BAD CODE ENDS HERE.
# (though what comes next is not particularly remarkable.)


@app.route('/login/', methods=['GET', 'POST'])
def login_router():
    if request.method == 'POST':
        if request.form['username'] in user_data:
            redirect_url = 'user/{}/dashboard'.format(request.form['username'])
            return redirect(redirect_url)
        else:
            error = "Login Failed! Please check login credentials."
            return render_template("login.html", title="Login", error=error)
    else:
        return render_template("login.html", title="Login")


@app.route('/user/<username>/dashboard/')
def dashboard_router(username):
    acc_type = user_data[username]['acc']
    page_title = "Dashboard - {} ".format(username)
    if acc_type == 'STU':
        return render_template("dashboard_student.html", title=page_title,\
                user=user_data[username])
    elif acc_type == "FAC":
        return render_template("dashboard_faculty.html", title=page_title,\
                user=user_data[username])
    else:
        return render_template("dashboard.html", title=page_title,\
                user=user_data[username])


@app.route('/user/<username>/dashboard/add_score/', methods=['GET', 'POST'])
def score_adder(username):
    if user_data[username]['acc'] != 'FAC':
        return render_template("non_response.html",
                title="Error: Not Authorized",
                user=user_data[username])
    if request.method == 'POST':
        print(request.form)
        for form_field in request.form:
            if form_field.split('_')[0] == 'score':
                student_name = form_field.split('_')[1]
                student_scores[student_name] = request.form[form_field]
        page_title = "{} - View Student Scores".format(username)
        sent_scores = [
            {   'name':user_data[username]['name'],
                'score':student_scores[username]}
                for username in student_scores]
        return render_template("show_scores.html", title=page_title, scores=sent_scores, user=user_data[username])
    else:
        page_title = "{} - Add Scores".format(username)
        student_list = [user_data[uname] for uname in user_data \
                            if user_data[uname]['acc'] == 'STU']
        return render_template("add_scores.html", title=page_title, students=student_list, user=user_data[username])

# THESE ROUTERS HAVE RECEIVED ENLIGHTENMENT.
# FOR THEY DON'T OVER COMPLICATE THINGS.
@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html", title="Home")

@app.route('/about/')
def about():
    return render_template("about.html", title="About")


# ERROR PAGE ROUTING
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
