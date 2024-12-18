# Copyright 2011 - 2019 Patrick Ulbrich <zulu99@gmx.net>
# Copyright 2016, 2024 Timo Kankare <timo.kankare@iki.fi>
# Copyright 2016 Thomas Haider <t.haider@deprecate.de>
# Copyright 2011 Ralf Hersel <ralf.hersel@gmx.net>
# Copyright 2019 razer <razerraz@free.fr>
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

"""Implementation for POP3 mailbox connection."""

import email
import logging
import poplib
from email.message import Message
from typing import Any, Iterator, Optional

from Mailnag.backends.base import MailboxBackend
from Mailnag.common.exceptions import InvalidOperationException


class POP3MailboxBackend(MailboxBackend):
	"""Implementation of POP3 mail boxes."""
	
	def __init__(
		self,
		name: str = '',
		user: str = '',
		password: str = '',
		oauth2string: str = '',
		server: str = '',
		port: str = '',
		ssl: bool = True,
		**kw
	):
		self.name = name
		self.user = user
		self.password = password
		self.oauth2string = oauth2string
		self.server = server
		self.port = port
		self.ssl = ssl # bool
		self._conn: Optional[poplib.POP3] = None


	def open(self) -> None:
		if self._conn != None:
			raise InvalidOperationException("Account is aready open")
				
		conn: Optional[poplib.POP3] = None
		
		try:
			if self.ssl:
				if self.port == '':
					conn = poplib.POP3_SSL(self.server)
				else:
					conn = poplib.POP3_SSL(self.server, int(self.port))
			else:
				if self.port == '':
					conn = poplib.POP3(self.server)
				else:
					conn = poplib.POP3(self.server, int(self.port))
				
				try:
					conn.stls()
				except:
					logging.warning("Using unencrypted connection for account '%s'" % self.name)
				
			conn.getwelcome()
			conn.user(self.user)
			conn.pass_(self.password)
		except:
			try:
				if conn is not None:
					conn.quit()
			except: pass
			raise # re-throw exception
		
		self._conn = conn


	def close(self) -> None:
		if self._conn is not None:
			self._conn.quit()
			self._conn = None


	def is_open(self) -> bool:
		return (self._conn != None) and \
				('sock' in self._conn.__dict__)


	def list_messages(self) -> Iterator[tuple[str, Message, dict[str, Any]]]:
		self._ensure_open()
		assert self._conn is not None
		conn = self._conn
		folder = ''
		
		# number of mails on the server
		mail_total = len(conn.list()[1])
		for i in range(1, mail_total + 1): # for each mail
			try:
				# header plus first 0 lines from body
				message = conn.top(i, 0)[1]
			except:
				logging.debug("Couldn't get POP message.")
				continue
			
			# convert list to byte sequence
			message_bytes = b'\n'.join(message)
			
			try:
				msg = email.message_from_bytes(message_bytes)
			except:
				logging.debug("Couldn't get msg from POP message.")
				continue
			yield (folder, msg, {})


	def request_folders(self) -> list[str]:
		raise NotImplementedError("POP3 does not support folders")


	def supports_mark_as_seen(self) -> bool:
		return False


	def mark_as_seen(self, mails: Any) -> bool:
		raise NotImplementedError


	def notify_next_change(self, callback: Any = None, timeout: Any = None) -> None:
		raise NotImplementedError("POP3 does not support notifications")


	def cancel_notifications(self) -> None:
		raise NotImplementedError("POP3 does not support notifications")


	def _ensure_open(self) -> None:
		if not self.is_open():
			raise InvalidOperationException("Account is not open")
