import os
import signal
import daemon
import lockfile
from test_app.app import app


context = daemon.DaemonContext(
    working_directory='/var/lib/runserver',
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/notificator.pid'),
    )

context.signal_map = {
    signal.SIGTERM: program_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: reload_program_config,
    }

context.uid = os.getuid()

log_file = open('log.log', 'w')
context.files_preserve = [log_file]

with context:
    app.run()
