from flask import Flask

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
