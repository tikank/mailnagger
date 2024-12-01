# Copyright 2024 Timo Kankare <timo.kankare@iki.fi>
# Copyright 2019 Patrick Ulbrich <zulu99@gmx.net>
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


from typing import Self, ClassVar, Optional
try:
	import gi
	gi.require_version('Secret', '1')
	from gi.repository import Secret
	_libsecret_err: ModuleNotFoundError | None = None
except ModuleNotFoundError as e:
	_libsecret_err = e


class SecretStore:
	_instance: ClassVar[Self | None] = None
	
	def __init__(self) -> None:
		if _libsecret_err is not None:
			raise _libsecret_err

		self._schema = Secret.Schema.new(
			'com.github.pulb.mailnag',  # Temporary fix to use Mailnags passwords.
			Secret.SchemaFlags.NONE,
			{'id' : Secret.SchemaAttributeType.STRING}
		)


	def get(self, secret_id: str) -> str:
		return Secret.password_lookup_sync(self._schema, {'id': secret_id}, None)


	def set(self, secret_id: str, secret: str, description: str) -> None:
		Secret.password_store_sync(
			self._schema, {'id': secret_id}, Secret.COLLECTION_DEFAULT, 
			description, secret, None)


	def remove(self, secret_id: str) -> bool:
		return Secret.password_clear_sync(self._schema, {'id': secret_id}, None)
	
	
	@staticmethod
	def get_default() -> Optional["SecretStore"]:
		if _libsecret_err is not None:
			return None

		if SecretStore._instance is None:
			SecretStore._instance = SecretStore()

		return SecretStore._instance
