# Copyright 2020 Patrick Ulbrich <zulu99@gmx.net>
# Copyright 2016, 2024 Timo Kankare <timo.kankare@iki.fi>
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

"""Implementation of local mailboxes, like mbox and maildir."""

import mailbox
import os.path
from email.message import Message
from typing import Any, Iterator, Optional

from Mailnag.backends.base import MailboxBackend
from Mailnag.common.exceptions import InvalidOperationException


class MBoxBackend(MailboxBackend):
	"""Implementation of mbox mail boxes."""
	
	def __init__(self, name: str = '', path: Optional[str] = None, **kw):
		"""Initialize mbox mailbox backend with a name and path."""
		self._name = name
		self._path = path
		self._opened = False


	def open(self) -> None:
		"""'Open' mbox. (Actually just checks that mailbox file exists.)"""
		if self._path is None or not os.path.isfile(self._path):
			raise IOError('Mailbox {} does not exist.'.format(self._path))
		self._opened = True


	def close(self) -> None:
		"""Close mbox."""
		self._opened = False


	def is_open(self) -> bool:
		"""Return True if mailbox is opened."""
		return self._opened


	def list_messages(self) -> Iterator[tuple[str, Message, dict[str, Any]]]:
		"""List unread messages from the mailbox.
		Yields tuples (folder, message, flags) where folder is always ''.
		"""
		if self._path is None:
			raise InvalidOperationException(
				"Path is not defined for Mbox '{self._name}'"
			)
		mbox = mailbox.mbox(self._path, create=False)
		folder = ''
		try:
			for msg in mbox:
				if 'R' not in msg.get_flags():
					yield (folder, msg, {})
		finally:
			mbox.close()


	def request_folders(self) -> list[str]:
		"""mbox does not suppoert folders."""
		raise NotImplementedError("mbox does not support folders")


	def supports_mark_as_seen(self) -> bool:
		return False


	def mark_as_seen(self, mails: Any) -> None:
		# TODO: local mailboxes should support this
		raise NotImplementedError

		
	def notify_next_change(
		self,
		callback: Any = None,
		timeout: Optional[int] = None
	) -> None:
		raise NotImplementedError("mbox does not support notifications")


	def cancel_notifications(self) -> None:
		raise NotImplementedError("mbox does not support notifications")


class MaildirBackend(MailboxBackend):
	"""Implementation of maildir mail boxes."""

	def __init__(
		self,
		name: str = '',
		path: Optional[str] = None,
		folders: list[str] = [],
		**kw
	):
		"""Initialize maildir mailbox backend with a name, path and folders."""
		self._name = name
		self._path = path
		self._folders = folders
		self._opened = False


	def open(self) -> None:
		"""'Open' mailbox. (Actually just checks that maildir directory exists.)"""
		if self._path is None or not os.path.isdir(self._path):
			raise IOError('Mailbox {} does not exist.'.format(self._path))
		self._opened = True


	def close(self) -> None:
		"""Close mailbox."""
		self._opened = False


	def is_open(self) -> bool:
		"""Return True if mailbox is opened."""
		return self._opened


	def list_messages(self) -> Iterator[tuple[str, Message, dict[str, Any]]]:
		"""List unread messages from the mailbox.
		Yields tuples (folder, message, flags).
		"""
		if self._path is None:
			raise InvalidOperationException(
				"Path is not defined for Maildir '{self._name}'"
			)
		folders = self._folders if len(self._folders) != 0 else ['']
		root_maildir = mailbox.Maildir(self._path, factory=None, create=False)
		try:
			for folder in folders:
				maildir = self._get_folder(root_maildir, folder)
				for msg in maildir:
					if 'S' not in msg.get_flags():
						yield folder, msg, {}
		finally:
			root_maildir.close()


	def request_folders(self) -> list[str]:
		"""Lists folders from maildir."""
		if self._path is None:
			raise InvalidOperationException(
				"Path is not defined for Maildir '{self._name}'"
			)
		maildir = mailbox.Maildir(self._path, factory=None, create=False)
		try:
			return [''] + maildir.list_folders()
		finally:
			maildir.close()


	def mark_as_seen(self, mails: Any) -> None:
		# TODO: local mailboxes should support this
		raise NotImplementedError


	def notify_next_change(
		self,
		callback: Any = None,
		timeout: Optional[int] = None
	) -> None:
		raise NotImplementedError("maildir does not support notifications")


	def cancel_notifications(self) -> None:
		raise NotImplementedError("maildir does not support notifications")


	def _get_folder(
		self,
		maildir: mailbox.Maildir,
		folder: str
	) -> mailbox.Maildir:
		"""Returns folder instance of the given maildir."""
		if folder == '':
			return maildir
		else:
			return maildir.get_folder(folder)

