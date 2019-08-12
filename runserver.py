from test_app.app import app
from test_app.extensions import db
from test_app.user.models import User
from test_app.reminder.reminder import run_reminder


run_reminder(3, db, User)
