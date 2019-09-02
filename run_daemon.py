import os
import daemon
import lockfile
import schedule
import time

from test_app.reminder.send_notifications import send_notifications

context = daemon.DaemonContext(
    working_directory='/vagrant',
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/notificator.pid'),
    )

# context.signal_map = {
#     signal.SIGTERM: program_cleanup,
#     signal.SIGHUP: 'terminate',
#     signal.SIGUSR1: reload_program_config,
#     }

context.uid = os.getuid()

log_file = open('log.log', 'r+')
context.files_preserve = [log_file]

with daemon.DaemonContext():
    schedule.every(1).minute.do(send_notifications)
    while 1:
        schedule.run_pending()
        time.sleep(1)
