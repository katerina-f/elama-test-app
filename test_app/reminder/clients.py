from abc import ABC
from abc import abstractmethod
import json
from threading import Thread
from datetime import datetime

from flask_mail import Message
from flask import render_template
from test_app.app import app
from test_app.app import mail
from test_app.app import logger

import pika

"""Шаблоны для отправки в разные клиенты."""

class AbstractClient(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def callback(self, *args, **kwargs):
        pass

    def parsing_request(self, body):
        msg_body = json.loads(body)
        return msg_body

    @abstractmethod
    def subscribe_to_queue(self):
        pass


class EmailClient(AbstractClient):
    def __init__(self):
        pass

    @logger.catch(level='ERROR')
    def update(self, message, recipients):
        with app.app_context():
            msg = Message('Birthdays', sender='katyfr0lova@yandex.ru', recipients=recipients)
            msg.html = render_template('birthdays.html', users_list=message)
            try:
                mail.send(msg)
            except:
                print('something wrong', datetime.now())

    def callback(self, ch, method, properties, body):
        recipients = ['ekaterina.frolova40@gmail.com', 'katyfr0lova@yandex.ru']
        msg_body = self.parsing_request(body)
        thr = Thread(target=self.update, args=[msg_body, recipients])
        thr.start()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def subscribe_to_queue(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue=__class__.__name__, durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(__class__.__name__, self.callback, auto_ack=False)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()


class SMSClient(AbstractClient):
    def __init__(self):
        pass

    def callback(self, *args, **kwargs):
        pass

    def update(self):
        pass


class SlackClient(AbstractClient):
    def __init__(self):
        pass

    def callback(self, *args, **kwargs):
        pass

    def update(self):
        pass
