from datetime import datetime

import schedule
from loguru import logger
from sqlalchemy import and_
from sqlalchemy import extract

from test_app.app import app


class Searcher:

    def __init__(self, db=None, model=None, days_before=3):
        self.session = db.session
        self.obj = model
        self.interval = days_before


    def bd_prompt_today(self):
        with app.app_context():
            users = self.obj.query.filter(and_(
                extract('day', self.obj.birth_date) == datetime.today().day,
                extract('month', self.obj.birth_date) == datetime.today().month))

            users = [{'date': '{}'.format(user.birth_date), 'name': '{}'.format(user.email)} for user in users]
            return users

    def bd_prompt_3_days(self, db):
        pass


def run_reminder(days_before, db, obj):
    searcher = Searcher(db, obj, days_before)
    searcher.bd_prompt_today()

