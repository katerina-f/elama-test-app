from flask import Flask

from test_app.user.models import User


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


@app.route('/')
def ping():
    return 'OK', 200


@app.route('/user')
def get_user():
    user = User.query.get(1)
    return user
