# Copyright 2024 Timo Kankare <timo.kankare@iki.fi>
# Copyright 2012 - 2020 Patrick Ulbrich <zulu99@gmx.net>
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


"""dist_cfg contains constants that may need to be adjusted for
   propper distro integration."""

import sysconfig
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path

# Application version displayed in the 
# about dialog of the config window.
APP_VERSION = '2.4.0.dev0'

# The PACKAGE_NAME constant is used to configure
# 1) the path where all app data (glade files, images) is loaded from
#    (usually /usr/share/<PACKAGE_NAME>) via get_data_file() (see utils.py). 
# 2) paths for localization files generated with gen_locales
#    (usually /usr/share/locale/<LANG>/LC_MESSAGES/<PACKAGE_NAME>.mo).
# Typically, there's no need to touch this constant.
PACKAGE_NAME = 'mailnagger'

# Default directories
_prefix = Path(sysconfig.get_path("data"))
_script_dir = Path(sysconfig.get_path('scripts'))
_DEFAULT_DATA_DIR = _prefix / "share" / PACKAGE_NAME
_DEFAULT_LOCALE_DIR = _prefix / "share" / "locale"
_DEFAULT_DESKTOP_FILE_DIR = _prefix / 'share' / 'applications'
_DEFAULT_LIB_DIR = files("Mailnag")
_DEFAULT_PLUGIN_DIR = files("Mailnag") / "plugins"
_DEFAULT_BIN_DIR = _script_dir

# The DATA_DIR specifies the root path for mailnagger data files
# (usually you have to make it pont to '/usr/share/mailnagger').
DATA_DIR: Path = _DEFAULT_DATA_DIR

# The LOCALE_DIR constant specifies the root path for localization files
# (usually you have to make it point to '/usr/share/locale').
LOCALE_DIR: Path = _DEFAULT_LOCALE_DIR

# The DESKTOP_FILE_DIR constant specifies the root path for .desktop files
# (usually you have to make it point to '/usr/share/applications').
DESKTOP_FILE_DIR: Path = _DEFAULT_DESKTOP_FILE_DIR

# The PLUGIN_DIR constant specifies the root path for the mailnagger plugin
# files (usually you have to make it point to <PYTHON_LIB_DIR>/Mailnag/plugins).
PLUGIN_DIR: Traversable | Path = _DEFAULT_PLUGIN_DIR

# The BIN_DIR constant specifies the path for the mailnag start scripts
# (usually you have to make it point to '/usr/bin').
BIN_DIR: Path = _DEFAULT_BIN_DIR

# DBUS service configuration
DBUS_BUS_NAME = 'mailnag.MailnagService'
DBUS_OBJ_PATH = '/mailnag/MailnagService'
