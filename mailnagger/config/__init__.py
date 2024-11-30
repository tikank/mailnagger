# Copyright 2024 Timo Kankare <timo.kankare@iki.fi>
# Copyright 2011 - 2019 Patrick Ulbrich <zulu99@gmx.net>
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

"""Configuration main function and configuration application."""


import gi
gi.require_version('Gtk', '3.0')

import os
import subprocess
import logging
from gi.repository import Gtk

from Mailnag.common.utils import init_logging
from Mailnag.common.utils import set_procname, shutdown_existing_instance
from Mailnag.common.dist_cfg import BIN_DIR
from Mailnag.configuration.configwindow import ConfigWindow
from mailnagger.resources import get_icon_paths

LOG_LEVEL = logging.DEBUG


class App(Gtk.Application):
    """Mailnagger config Gtk application."""

    def __init__(self):
        Gtk.Application.__init__(self, application_id = 'com.github.tikank.mailnagger')
        self.win = None


    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)

        # Add icons in alternative data paths (e.g. ./data/icons) 
        # to the icon search path in case Mailnag is launched 
        # from a local directory (without installing).
        icon_theme = Gtk.IconTheme.get_default()
        for path in get_icon_paths():
            icon_theme.append_search_path(str(path))

    def do_activate(self) -> None:
        Gtk.Application.do_activate(self)

        if not self.win:
            self.win = ConfigWindow(self)
        self.win.get_gtk_window().present()


    def do_shutdown(self) -> None:
        Gtk.Application.do_shutdown(self)

        if self.win.get_daemon_enabled():
            try:
                # the launched daemon shuts down 
                # an already running daemon
                print("Launching Mailnagger daemon.")
                subprocess.Popen(os.path.join(BIN_DIR, "mailnagger"))
            except Exception as e:
                print(f"ERROR: Failed to launch Mailnagger daemon: {str(e)}")
        else:
            # shutdown running Mailnagger daemon
            shutdown_existing_instance(wait_for_completion = False)


def main() -> int:
    """Mailnagger config main function."""

    set_procname("mailnagger-config")
    init_logging(enable_stdout = True, enable_syslog = False, log_level = LOG_LEVEL)
    app = App()
    app.run(None)
    return os.EX_OK

