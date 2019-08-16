from abc import ABC
from abc import abstractmethod
import time

from flask_mail import Message

import pika

"""Шаблоны для отправки в разные клиентыю
Дальше предполагается подписка на очередь и обработка сообщений из нее"""

class AbstractClient(ABC):
    @abstractmethod
    def update(self):
        pass


class EmailClient(AbstractClient):
    def __init__(self):
        pass

    def parsing(self, connection):
        channel = connection.channel()

        channel.queue_declare(queue=self.__str__(), durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(body)
            time.sleep(2)
            print(" [x] Done")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.__str__(), callback, auto_ack=False)

        channel.start_consuming()


    def update(self):
        pass


class SMSClient(AbstractClient):
    def __init__(self):
        pass

    def parsing(self, data):
        pass

    def update(self):
        pass


class SlackClient(AbstractClient):
    def __init__(self):
        pass

    def parsing(self, data, queue):
        pass

    def update(self):
        pass
