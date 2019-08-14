from flask import request
from flask import render_template
from flask import jsonify
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import DataError
from sqlalchemy.exc import IntegrityError

from test_app.app import app
from test_app.user.models import User

from test_app.reminder.reminder import BdayNotificator

from test_app.extensions import db


@app.route('/')
def ping():
    return 'OK', 200


@app.route('/users')
def get_user():
    """
    Отображает всех пользователей, находящихся в базе
    """
    users = User.query.order_by(User.last_name)
    list = {'{} {}:{}'.format(user.first_name, user.last_name, user.birth_date) for user in users}
    return '{}'.format(list)


@app.route('/add_user', methods=['GET'])
def add_user():
    return render_template('user.html')


@app.route('/added_user', methods=['POST'])
def added_user():
    user = User(first_name=request.form['First name'], last_name=request.form['Last name'], birth_date=request.form['birthday'])
    db.session.add(user)
    try:
        db.session.commit()
    except OperationalError as ex:
        db.session.rollback()
        return jsonify({'error': "Bad connection. Try again later."})
    except DataError as ex:
        db.session.rollback()
        return jsonify({'error': "Data Format Error"})
    except IntegrityError as ex:
        db.session.rollback()
        return jsonify({'error': "User already exists"})

    return 'USER {} {} added successfully'.format(user.first_name, user.last_name)


@app.route('/get_birthdays', methods=['GET'])
def create_notification():
    notificator = BdayNotificator(db, User, interval=(0, 1))
    data = notificator.bd_prompt()
    if any(data):
        return render_template('birthdays.html', users_list=data)
    else:
        message = 'Пока поздравлять некого!'
        return render_template('birthdays.html', message=message)
