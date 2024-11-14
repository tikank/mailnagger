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
    name='tests-default',
    venv_backend='venv',
)
def tests_default(session : nox.Session) -> None:
    """Run unit tests with default python."""
    tests(session)


@nox.session(
    python=['3.13', '3.12'],
    venv_backend='venv',
)
def tests(session : nox.Session) -> None:
    """Run unit tests"""
    session.install('.')
    session.install('pytest')
    session.run('python', '-m', 'pytest')


@nox.session
def mypy(session : nox.Session) -> None:
    """Run mypy type checker."""
    session.install('mypy')
    session.run('python', '-m', 'mypy')


@nox.session
def flake8(session : nox.Session) -> None:
    """Run flake8"""
    session.install('flake8')
    session.run('python', '-m', 'flake8', '--statistics')


@nox.session(
    default=False,
)
def build(session : nox.Session) -> None:
    """Build sdist and wheel packages to dist."""
    session.install("build")
    session.run("python", "-m", "build")


@nox.session(
    default=False,
)
def dev(session : nox.Session) -> None:
    """Set up a python development environment for the project at .env-dev."""

    env = ".env-dev"

    session.run("python", "-m", "venv", "--clear", env)

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensures it's installed in the right way
    session.run(env + "/bin/python", "-m", "pip", "install", "-e", ".", external=True)
    print("Activate environment: . " + env + "/bin/activate")

