# Copyright 2024 Timo Kankare <timo.kankare@iki.fi>
# Copyright 2011 - 2019 Patrick Ulbrich <zulu99@gmx.net>
# Copyright 2007 Marco Ferragina <marco.ferragina@gmail.com>
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

import sys
import time
import dbus
import logging
import logging.handlers


from Mailnag.common.dist_cfg import DBUS_BUS_NAME, DBUS_OBJ_PATH

LOG_FORMAT = '%(levelname)s (%(asctime)s): %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def init_logging(enable_stdout = True, enable_syslog = True, log_level = logging.DEBUG):
	logging.basicConfig(
		format = LOG_FORMAT,
		datefmt = LOG_DATE_FORMAT,
		level = log_level)
	
	logger = logging.getLogger('')
	
	if not enable_stdout:
		stdout_handler = logger.handlers[0]
		logger.removeHandler(stdout_handler)
	
	if enable_syslog:
		syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
		syslog_handler.setLevel(log_level)
		syslog_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
	
		logger.addHandler(syslog_handler)


def splitstr(strn, delimeter):
	return [s.strip() for s in strn.split(delimeter) if s.strip()]


def set_procname(newname):
	from ctypes import cdll, byref, create_string_buffer
	libc = cdll.LoadLibrary('libc.so.6')
	buff = create_string_buffer(len(newname)+1)
	buff.value = newname.encode('utf-8')
	libc.prctl(15, byref(buff), 0, 0, 0)


def try_call(f, err_retval = None):
	try:
		return f()
	except:
		logging.exception('Caught an exception.')
		return err_retval


def shutdown_existing_instance(wait_for_completion = True):
	bus = dbus.SessionBus()
	
	if bus.name_has_owner(DBUS_BUS_NAME):
		sys.stdout.write('Shutting down existing Mailnagger process...')
		sys.stdout.flush()
		
		try:
			proxy = bus.get_object(DBUS_BUS_NAME, DBUS_OBJ_PATH)
			shutdown = proxy.get_dbus_method('Shutdown', DBUS_BUS_NAME)
			
			shutdown()
			
			if wait_for_completion:
				while bus.name_has_owner(DBUS_BUS_NAME):
					time.sleep(2)
			
			print('OK')
		except:
			print('FAILED')
