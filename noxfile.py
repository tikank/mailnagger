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

import nox


@nox.session(
    python=['3.12'],
    venv_backend='venv',
)
def tests(session):
    """Run unit tests"""
    session.install('pygobject')
    session.install('pyxdg')
    session.install('dbus-python')
    session.install('.')
    session.install('pytest')
    session.run('python', '-m', 'pytest')


@nox.session(
    python=['3.12'],
    venv_backend='venv',
    venv_params=['--system-site-packages'],
)
def tests_with_system_site(session):
    """Run unit tests (with system-site-packages)"""
    session.install('.')
    session.install('pytest')
    session.run('python', '-m', 'pytest')



