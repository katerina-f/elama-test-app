from datetime import datetime
from datetime import timedelta
import sys


from sqlalchemy import and_
from sqlalchemy import extract

import pika


class BdayFinder:

    def __init__(self, model=None, interval=()):
        self.obj = model
        self.interval = interval

    def find_users_for_date(self, remind_date):
        date = datetime.today() + timedelta(days=remind_date)

        b_day = extract('day', self.obj.birth_date)
        b_month = extract('month', self.obj.birth_date)

        users = self.obj.query.filter(and_(b_day == date.day, b_month == date.month))

        users = [{'bdate': '{}'.format(user.birth_date),
                  'first_name': '{}'.format(user.first_name),
                  'last_name': '{}'.format(user.last_name),
                  'days_to_birthday': remind_date} for user in users]
        return users

    def creating_users_list(self):
        users_list = [self.find_users_for_date(date) for date in self.interval]
        if any(users_list):
            return users_list
        else:
            return []


class Postman:

    def __init__(self, notification_time='09:00'):
        self.subscribers = set()
        self.notification_time = notification_time  #<type 'str'>

    def get_data(self, interval, obj, connection):
        finder = BdayFinder(obj, interval)
        result = finder.creating_users_list()
        if result:
            self.notify(connection, result)

        return result

    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubcribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def create_queue(self, subscriber, connection):
        channel = connection.channel()
        channel.queue_declare(queue=subscriber.__str__(), durable=True)

        return channel

    def notify(self, connection, message):
        for subscriber in self.subscribers:
            channel = self.create_queue(subscriber, connection)
            channel.basic_publish(exchange='',
                                  routing_key=subscriber.__name__,
                                  body=message,
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,  # make message persistent
                                  ))
