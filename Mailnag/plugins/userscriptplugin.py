# Copyright 2013 - 2020 Patrick Ulbrich <zulu99@gmx.net>
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

import gi
gi.require_version('Gtk', '3.0')

import os
from gi.repository import Gtk
from Mailnag.common.plugins import Plugin, HookTypes
from Mailnag.common.i18n import _
from Mailnag.common.subproc import start_subprocess

plugin_defaults = {'script_file' : ''}


class UserscriptPlugin(Plugin):
	def __init__(self):
		self._mails_added_hook = None

	
	def enable(self):
		def mails_added_hook(new_mails, all_mails):
			self._run_userscript(new_mails)
		
		self._mails_added_hook = mails_added_hook
		
		controller = self.get_mailnag_controller()
		hooks = controller.get_hooks()
		
		hooks.register_hook_func(HookTypes.MAILS_ADDED, 
			self._mails_added_hook)
		
	
	def disable(self):
		controller = self.get_mailnag_controller()
		hooks = controller.get_hooks()
		
		if self._mails_added_hook != None:
			hooks.unregister_hook_func(HookTypes.MAILS_ADDED,
				self._mails_added_hook)
			self._mails_added_hook = None

	
	def get_manifest(self):
		return (_("User Script"),
				_("Runs an user defined script on mail arrival."),
				"2.0",
				"Patrick Ulbrich <zulu99@gmx.net>")


	def get_default_config(self):
		return plugin_defaults
	
	
	def has_config_ui(self):
		return True
	
	
	def get_config_ui(self):
		box = Gtk.Box()
		box.set_spacing(12)
		box.set_orientation(Gtk.Orientation.VERTICAL)
		# box.set_size_request(100, -1)
		
		markup_str = "<i>&lt;%s&gt; &lt;%s&gt; &lt;%s&gt;</i>" % (_('account'), _('sender'), _('subject'))
		desc = _("The following script will be executed whenever new mails arrive.\n"
				"Mailnagger passes the total count of new mails to this script,\n"
				"followed by %s sequences.") % markup_str
		
		label = Gtk.Label()
		label.set_line_wrap(True)
		label.set_markup(desc)
		# label.set_size_request(100, -1);
		box.pack_start(label, False, False, 0)
		
		filechooser = Gtk.FileChooserButton()
		box.pack_start(filechooser, False, False, 0)
		
		return box
	
	
	def load_ui_from_config(self, config_ui):
		config = self.get_config()
		script_file = config['script_file']
		if len(script_file) > 0:
			filechooser = config_ui.get_children()[1]
			filechooser.set_filename(script_file)
	
	
	def save_ui_to_config(self, config_ui):
		config = self.get_config()
		filechooser = config_ui.get_children()[1]
		script_file = filechooser.get_filename()
		if script_file == None: script_file = ''
		config['script_file'] = script_file
	
	
	def _run_userscript(self, new_mails):
		config = self.get_config()
		script_file = config['script_file'].strip()
		if (len(script_file) > 0) and os.path.exists(script_file):
			script_args = [script_file, str(len(new_mails))]
			
			for m in new_mails:
				sender_name, sender_addr = m.sender
				if len(sender_addr) == 0: sender_addr = 'UNKNOWN_SENDER'
				
				script_args.append(m.account.name)
				script_args.append(sender_addr)
				script_args.append(m.subject)
			start_subprocess(script_args)
