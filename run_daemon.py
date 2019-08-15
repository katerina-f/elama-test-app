import os
import signal
import daemon
import lockfile

from spam import (
    initial_program_setup,
    do_main_program,
    program_cleanup,
    reload_program_config,
    )

context = daemon.DaemonContext(
    working_directory='/',
    umask=0o002,
    pidfile=lockfile.FileLock('/notificator.pid'),
    )

context.signal_map = {
    signal.SIGTERM: program_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: reload_program_config,
    }

context.uid = os.getuid()

important_file = open('spam.data', 'w')
interesting_file = open('eggs.data', 'w')
context.files_preserve = [important_file, interesting_file]

initial_program_setup()

with context:
    do_main_program()
