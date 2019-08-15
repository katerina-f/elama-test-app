from abc import ABC
from abc import abstractmethod

"""Шаблоны для отправки в разные клиентыю
Дальше предполагается подписка на очередь и обработка сообщений из нее"""

class AbstractClient(ABC):
    @abstractmethod
    def update(self):
        pass


class EmailClient(AbstractClient):
    def __init__(self, queue):
        pass

    def parsing(self, data):
        pass

    def update(self):
        pass


class SMSClient(AbstractClient):
    def __init__(self, queue):
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
