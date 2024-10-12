![Mailnagger](data/icons/hicolor/256x256/apps/mailnag.png)

## An extensible mail notification daemon

Mailnagger is a daemon program that checks POP3 and IMAP servers for new mail.
On mail arrival it performs various actions provided by plugins.
Mailnagger comes with a set of desktop-independent default plugins for
visual/sound notifications, script execution etc. and can be extended
with additional plugins easily.

Mailnagger is a fork of [Mailnag](https://github.com/pulb/mailnag).

__This project needs your support!__

If you like Mailnagger, please help to keep it going by [contributing code](https://github.com/tikank/mailnagger),
[reporting/fixing bugs](https://github.com/tikank/mailnagger/issues),
[translating strings into your native language](https://github.com/tikank/mailnagger/tree/master/po),
or writing docs.


## Installation

### Generic Tarballs

Distribution independent tarball releases are available [here](https://github.com/tikank/mailnagger/releases).

Build Mailnagger by running

```
    ./setup build
```

Then run

```
    python3 -m pip install --break-system-packages .
```

(as root) to install Mailnagger system wide,
though make sure the requirements stated below are met.

###### Requirements

* python (>= 3.5)
* pygobject
* gir-notify (>= 0.7.6)
* gir-gtk-3.0
* gir-gdkpixbuf-2.0
* gir-glib-2.0
* gir-gst-plugins-base-1.0
* python-dbus
* pyxdg
* gettext
* gir1.2-secret-1 (optional)


### Distribution specific packages

Mailnagger is not packaged to any Linux distribution (yet).
If you make packaging or know one, let me know!

Mailnag used to be packaged to Ubuntu, Debian, Fedora, Arch Linux and openSUSE.


## Configuration

Run `mailnagger-config` to setup Mailnagger.

Closing the configuration window will start Mailnagger automatically.


### Default Mail Client

Clicking a mail notification popup will open the default mail client specified in `GNOME Control Center -> Details -> Default Applications`.
If you're a webmail (e.g. gmail) user and want your account to be launched in a browser, please install a tool like [gnome-gmail](http://gnome-gmail.sourceforge.net).


### Desktop Integration

By default, Mailnagger emits libnotify notifications, which work fine on
most desktop environments but are visible for a few seconds only.
If you like to have a tighter desktop integration (e.g. a permanently visible indicator in your top panel) you have to install an appropriate
extension/plugin for your desktop shell.

Mailnag has following desktop extensions:

* GNOME-Shell ([GNOME-Shell extension](https://github.com/pulb/mailnag-gnome-shell)) 
* KDE ([Plasma 5 applet by driglu4it](https://store.kde.org/p/1420222/))
* Cinnamon ([Applet by hyOzd](https://bitbucket.org/hyOzd/mailnagapplet))
* Elementary Pantheon ([MessagingMenu plugin](https://github.com/pulb/mailnag-messagingmenu-plugin))
* XFCE ([MessagingMenu plugin](https://github.com/pulb/mailnag-messagingmenu-plugin))

Since Mailnagger is essentially same as Mailnag, those extensions should/might
work with Mailnagger.

Furthermore, GNOME users can also install the [GOA plugin](https://github.com/pulb/mailnag-goa-plugin),
which makes Mailnagger aware of email accounts specified in GNOME Online Accounts.

### Troubleshooting

__Gmail doesn't work__

If Mailnagger is unable to connect to your Gmail account, please try the following solutions:
* Install the [GOA plugin](https://github.com/pulb/mailnag-goa-plugin) to connect via GNOME online accounts
* Have a look at the [FAQ](https://github.com/pulb/mailnag/wiki/FAQ)
* Try to apply [this](https://github.com/pulb/mailnag/issues/190) workaround

__Other issues__

If Mailnagger doesn't work properly for you, either examine the system log
for errors (`journalctl -b _COMM=mailnagger`)
or run `mailnagger` in a terminal and observe the output.
  
