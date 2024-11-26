
### Developing


#### Install in editable mode

For developing mailnagger can be installed in development mode.
Run nox command:

```
    nox -s dev
```

It creates virtual env to .env-dev directory and env can be activated with
command

```
    . .env-dev/bin/activate
```

Now mailnagger can be run with commands

```
    mailnagger-config
    mailnagger
```


#### Running from sources

I have moved mailnagger scripts to console scripts, so running mailnagger
from sources is not directly possible.

Instead mailnagger-config and mailnagger daemon can be run with commands

```
    python3 -m mailnagger.config
    python3 -m mailnagger
```

That works only partially.
Mailnagger config does not install autostart desktop entry and fails to start
mailnagger daemon.

