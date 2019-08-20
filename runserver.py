from test_app.app import app
from test_app import routes
import schedule
import time
from test_app.reminder.send_notifications import send_notifications

schedule.every(1).minutes.do(send_notifications)

while 1:
    schedule.run_pending()
    time.sleep(1)

