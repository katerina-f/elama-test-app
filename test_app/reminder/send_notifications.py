from test_app.reminder.reminder import Postman
from test_app.reminder.clients import EmailClient
from test_app.app import app
from test_app.user.models import User


def send_notifications():
    with app.app_context():
        notificator = Postman(app.config['NOTIFICATION_TIME'])
        notificator.subscribe(EmailClient)
        notificator.get_data(app.config['INTERVAL'], User)
        client = EmailClient()
        client.subscribe_to_queue()
