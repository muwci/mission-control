import csv

from flask import render_template

def authenticate_login(username, **kwargs):
    USER_DATA_FILE = "./app/data/userlogin.csv"
    user_data_reader = csv.reader(open(USER_DATA_FILE))
    headers = next(user_data_reader)
    usernames = [data[0] for data in user_data_reader]
    return username in usernames
