from datetime import datetime
from datetime import timedelta
import time

from flask import jsonify

import schedule
from loguru import logger
from sqlalchemy import and_
from sqlalchemy import extract

class BdayNotificator:

    def __init__(self, db=None, model=None, interval=(), app=None):
        self.session = db.session
        self.obj = model
        self.interval = interval
        self.app = app

    def find_needed_users(self, remind_date):
        date = datetime.today() - timedelta(days=remind_date)

        with self.app.app_context():
            users = self.obj.query.filter(and_(
                extract('day', self.obj.birth_date) == date.day,
                extract('month', self.obj.birth_date) == date.month))

            if not users:
                logger.warning('Сегодня дней рождения нет')

            users = [{'bdate': '{}'.format(user.birth_date),
                      'name': '{}'.format(user.email),
                      'days_to_birthday': '{}'.format(remind_date)} for user in users]
            return users

    def bd_prompt(self):
        users_list = [self.find_needed_users(date) for date in self.interval]
        return users_list

    def create_message(self, users):
        pass


# class Postman:
#
#     def __init__(self, notification_time='00:00'):
#         self.notification_time = notification_time  #<type 'str'>
#         # self.host = app.config['HOST']
#         # self.port = app.config['PORT']
#
#     def run_reminder(self, interval, db, obj):
#         notificator = BdayNotificator(db, obj, interval)
#         schedule.every().day.at(self.notification_time).do(notificator.bd_prompt)
#
#         while True:
#             schedule.run_pending()
#             time.sleep(1)


