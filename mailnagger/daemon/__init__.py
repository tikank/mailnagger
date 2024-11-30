# Copyright 2024 Timo Kankare <timo.kankare@iki.fi>
# Copyright 2011 - 2020 Patrick Ulbrich <zulu99@gmx.net>
# Copyright 2011 Leighton Earl <leighton.earl@gmx.com>
# Copyright 2011 Ralf Hersel <ralf.hersel@gmx.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

"""Daemon main function."""


import gi
gi.require_version('GLib', '2.0')

from gi.repository import GLib
from dataclasses import dataclass
from dbus.mainloop.glib import DBusGMainLoop
import threading
import argparse
import logging
import os
import signal

from Mailnag.common.config import cfg_exists
from Mailnag.common.dist_cfg import APP_VERSION
from Mailnag.common.utils import set_procname, init_logging, shutdown_existing_instance
from Mailnag.common.subproc import terminate_subprocesses
from Mailnag.common.exceptions import InvalidOperationException
from Mailnag.daemon.mailnagdaemon import MailnagDaemon

PROGNAME = 'mailnagger'
LOG_LEVEL = logging.DEBUG


def cleanup(daemon: MailnagDaemon | None) -> None:
    """Terminates the deamon subprocesses."""

    event = threading.Event()

    def thread() -> None:
        if daemon is not None:
            daemon.dispose()

        terminate_subprocesses(timeout = 3.0)
        event.set()

    threading.Thread(target = thread).start()
    event.wait(10.0)

    if not event.is_set():
        logging.warning('Cleanup takes too long. Enforcing termination.')
        os._exit(os.EX_SOFTWARE)

    if threading.active_count() > 1:
        logging.warning('There are still active threads. Enforcing termination.')
        os._exit(os.EX_SOFTWARE)


@dataclass
class Args:
    """Command line arguments."""
    quiet: bool = False


def get_args() -> Args:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(prog=PROGNAME)
    parser.add_argument('-q', '--quiet', action = 'store_true', 
        help = "don't print log messages to stdout")
    parser.add_argument('-v', '--version', action = 'version',
        version = '%s %s' % (PROGNAME, APP_VERSION))

    return parser.parse_args(namespace=Args())


def sigterm_handler(mainloop: GLib.MainLoop) -> bool:
    """Handler for TERM signal. Stops the main loop."""
    if mainloop is not None:
        mainloop.quit()
    return False


def main() -> int:
    """Mailnagger daemon main function."""
    mainloop = GLib.MainLoop()
    daemon = None

    set_procname(PROGNAME)

    DBusGMainLoop(set_as_default = True)
    GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGTERM, 
        sigterm_handler, mainloop)

    # Get commandline arguments
    args = get_args()

    # Shut down an (possibly) already running Mailnag daemon
    # (must be called before instantiation of the DBUSService).
    shutdown_existing_instance()

    # Note: don't start logging before an existing Mailnag 
    # instance has been shut down completely (will corrupt logfile).
    init_logging(
        enable_stdout = (not args.quiet),
        enable_syslog = True,
        log_level = LOG_LEVEL
    )

    try:
        if not cfg_exists():
            logging.critical(
                "Cannot find configuration file. " +
                "Please run mailnagger-config first.")
            exit(1)

        def fatal_error_hdlr(ex: Exception) -> None:
            # Note: don't raise an exception 
            # (e.g InvalidOperationException) 
            # in the error handler.
            mainloop.quit()

        def shutdown_request_hdlr() -> None:
            if not mainloop.is_running():
                raise InvalidOperationException(
                    "Mainloop is not running")
            mainloop.quit()

        # Initialize mailnag daemon and start checking threads
        daemon = MailnagDaemon(
            fatal_error_hdlr, 
            shutdown_request_hdlr)

        # start mainloop for DBus communication
        mainloop.run()

    except KeyboardInterrupt:
        pass # ctrl+c pressed
    finally:
        logging.info('Shutting down...')
        cleanup(daemon)

    return os.EX_OK

