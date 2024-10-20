### Install Mailnagger

#### System wide installation

Build Mailnagger

```
    python3 ./setup build
```

Then run as root

```
    python3 -m pip install --break-system-packages .
```

#### Installation to virtual env

The aim to support installation to virtual venv is to help run tests
automatically and support installation without root access.

> **NOTE:** Installation to virtual env works only partially. 
>           Soundplugin does not yet find sound file and all data files might
>           not be in correct place.

Build Mailnagger

```
    python3 ./setup build
```

Make virtualenv

```
    python3 -m venv --system-site-packages env
```

Then run as root

```
    ./env/bin/python3 -m pip install .
```

Running Mailnagger from virtual env

```
    ./env/bin/mailnagger-config
```

