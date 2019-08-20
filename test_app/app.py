from flask import Flask

from loguru import logger

from test_app.extensions import db
from test_app.extensions import mail
from test_app.config import DevelopmentConfig


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    logger.start(app.config['LOGFILE'], level=app.config['LOG_LEVEL'], backtrace=app.config['LOG_BACKTRACE'], format="{time} {level} {message}",
               rotation='1 week', catch=True)

    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)


app = create_app()
