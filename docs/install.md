### Install Mailnagger

Mailnagger can be installed from

* source dir, for example: `.`

* source package: `mailnagger-X.Y.Z.tar.gz`

* wheel package: `mailnagger-X.Y.Z-py3-none-any.whl`

* package from [PyPI](https://pypi.org/project/mailnagger/): `mailnagger`

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

> **Note:**
> Mailnagger conflict with Mailnag, because the code is not (yet) renamed.
> So don't install Mailnagger and Mailnag same time.

> **TODO:** Setup mailnagger-config.desktop file, etc. How?


#### Distribution specific packages

Mailnagger is not packaged to any Linux distribution (yet).
If you make packaging or know one, let me know!

Mailnag used to be packaged to Ubuntu, Debian, Fedora, Arch Linux and openSUSE.

