# -*- coding: utf-8 -*-
#
# noxfile.py
#
# Copyright 2019 Timo Kankare <timo.kankare@iki.fi>
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

"""Nox file to automate testing of Mailnag."""

import nox

nox.options.sessions = ['test-2.7']

@nox.session(python=['2.7', '3.7'])
def test(session):
	"""Run unit tests."""
	session.install('pytest')
	session.install('pyxdg', 'vext', 'vext.gi', 'vext.dbus')
	session.install('.')
	session.run('pytest')

