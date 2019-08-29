import time
import schedule

from test_app.app import app
from test_app.reminder.send_notifications import send_notifications
from test_app.app import logger


def main():
    try:
        schedule.every(2).minutes.do(send_notifications)

        while 1:
            schedule.run_pending()
            time.sleep(1)
    except Exception as ex:
        logger.warning(ex.__str__())

if __name__ == '__main__':
    with app.app_context():
        main()
