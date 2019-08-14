from flask import request
from flask import render_template

from test_app.app import app
from test_app.user.models import User

from test_app.reminder.reminder import BdayNotificator

from test_app.extensions import db


@app.route('/')
def ping():
    return 'OK', 200


@app.route('/user')
def get_user():
    users = User.query.all()
    list = {'{}:{}'.format(user.email, user.birth_date) for user in users}
    return '{}'.format(list)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/get_params', methods=['POST'])
def get_params():
    user = User(email=request.form['email'], password=request.form['password'], birth_date=request.form['birthday'])
    db.session.add(user)
    db.session.commit()
    return 'USER {} added successfully'.format(user.email)


@app.route('/get_birthdays', methods=['GET'])
def create_notification():
    notificator = BdayNotificator(db, User, interval=(0, 1))
    data = notificator.bd_prompt()
    if any(data):
        return render_template('birthdays.html', users_list=data)
    else:
        message = 'Пока поздравлять некого!'
        return render_template('birthdays.html', message=message)
