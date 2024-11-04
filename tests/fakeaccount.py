# Copyright 2024 Timo Kankare <timo.kankare@iki.fi>
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

"""Fake accoun and backend to support unit tests."""

import email
from Mailnag.common.accounts import Account
from Mailnag.backends.base import MailboxBackend


class FakeBackend(MailboxBackend):
	"""Fake mailbox backend implementation for testing."""

	def __init__(self, **kw):
		self._opened = False
		self.messages = []


	def open(self):
		self._opened = True


	def close(self):
		self._opened = False


	def is_open(self):
		return self._opened


	def list_messages(self):
		for msg in self.messages:
			m = email.message_from_string(msg)
			print(m)
			yield "samplefolder", m, {}


	def mark_as_seen(self, mails):
		raise NotImplementedError


	def request_folders(self):
		raise NotImplementedError("no folder support")


	def notify_next_change(self, callback=None, timeout=None):
		raise NotImplementedError("no notification support")


	def cancel_notifications(self):
		raise NotImplementedError("no notification support")


class FakeAccount(Account):
	"""Fake account implementation to use special test backend."""

	def __init__(self, **kw):
		Account.__init__(self, **kw)
		self._backend = FakeBackend()


	def set_current_messages(self, messages):
		self._backend.messages = messages

