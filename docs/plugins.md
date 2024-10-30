### Plugins

There is some build-in plugins included in mailnagger package

* libnotify plugin shows new mails in desktop notifiation area.

* soundplugin says "ping" when new mail arrives.

* spamfilter finds words from the subject and sender fields,
  and ignores mails from notifications.

* userscript runs user defined program when new mail arrives.


#### Plugin achitecture

Plugin component implements `Mailnag.common.plugins.Plugin` interface.
Plugin registers hooks (callbacks) and Mailnagger notifies then when something
happens.

Available hook types are:

* Account loaded, called when mailnagger starts.
* Mail check, called when mailnagger starts to check mails.
* Filter mails, called when mails are checked.
* Mails added, called when new mail arrives.
* Mails removed, called when user has read the mail or marked it as seen.

Plugin modules are searched from mailnagger configuration directory,
currently `~/.config/mailnag/plugins`.

