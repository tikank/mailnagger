
## Notes about developing Mailnag

### Running unit tests

Unit tests are located in the tests directory.
Running unit tests requires [pytest](https://pypi.org/project/pytest/):

    python -m pytest


### Running unit tests with Nox

noxfile.py defines how [Nox](https://pypi.org/project/nox/) create
Python virtualenv, install Mailnag, and run tests.

To run tests with Nox use command

    nox

or

    nox -r

Note:
Since Mailnag depends on system libraries which cannot be installed
to virtualenv, noxfile installs [vext](https://pypi.org/project/vext/),
vext.gi and [vext.dbus](https://pypi.org/project/vext.dbus/). They allow
the usage of gi and dbus system libraries from virtualenv.

