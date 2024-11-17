### Install Mailnagger

Mailnagger can be installed from

* source dir, for example: `.`

* source package: `mailnagger-X.Y.Z.tar.gz`

* wheel package: `mailnagger-X.Y.Z-py3-none-any.whl`

* package from [PyPi}(https://pypi.org/): `mailnagger`
  (**NOTE/TODO:** Not yet but someday in future!)

Replace `mailnagger` with one of previous in following examples.


#### Installing with pipx

[pipx](https://pypi.org/project/pipx/) is a tool to install Python
applications to isolated environment.
This is recommented way to install mailnagger without root access.

Run

```
    pipx install mailnagger
```


#### Installation to virtual env

The aim to support installation to virtual venv is to help run tests
automatically and support installation without root access.

Make virtualenv

```
    python3 -m venv env
```

Then run

```
    ./env/bin/python -m pip install mailnagger
```

Running Mailnagger from virtual env

```
    ./env/bin/mailnagger-config
```


#### System wide installation

System wide installation requires root access rights.

Run as root

```
    python3 -m pip install --break-system-packages mailnagger
```

> **TODO:** Setup mailnagger-config.desktop file, etc. How?

