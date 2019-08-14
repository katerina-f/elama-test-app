from datetime import datetime
from datetime import timedelta

from loguru import logger
from sqlalchemy import and_
from sqlalchemy import extract


class BdayNotificator:

    def __init__(self, db=None, model=None, interval=()):
        self.session = db.session
        self.obj = model
        self.interval = interval

    def find_needed_users(self, remind_date):
        date = datetime.today() + timedelta(days=remind_date)

        b_day = extract('day', self.obj.birth_date)
        b_month = extract('month', self.obj.birth_date)

        users = self.obj.query.filter(and_(b_day == date.day, b_month == date.month))

        if not users:
            logger.warning('Сегодня дней рождения нет')
            return []

        users = [{'bdate': '{}'.format(user.birth_date),
                  'name': '{}'.format(user.email),
                  'days_to_birthday': remind_date} for user in users]

        return users

    def bd_prompt(self):
        users_list = [self.find_needed_users(date) for date in self.interval]
        if any(users_list):
            return users_list
        else:
            return []

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


