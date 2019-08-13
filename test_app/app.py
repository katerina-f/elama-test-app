from flask import Flask
from flask import request
from flask import render_template

from test_app.user.models import User
from test_app.post.models import Post
from test_app.reminder.reminder import BdayNotificator

from test_app.extensions import db


def create_app():
    app = Flask(__name__)
    app.secret_key = '478fdh5j7ghh7778548954jkd89dd9de9d9'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        'test', '1234', 'localhost', 'postgres'
    )
    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)


app = create_app()


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
    notificator = BdayNotificator(db, User, interval=(0, 1), app=app)
    users_list = notificator.bd_prompt()
    return render_template('birthdays.html', users_list=users_list)
