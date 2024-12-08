# Copyright 2024 Timo Kankare <timo.kankare@iki.fi>
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


import os
import importlib.util
import importlib.machinery
import inspect
import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from configparser import RawConfigParser
from enum import Enum
from typing import Any, Optional
from mailnagger.resources import get_plugin_paths

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


#
# All known hook types.
#
class HookTypes(Enum):
	# func signature: 
	# IN:	List of loaded accounts
	# OUT:	None
	ACCOUNTS_LOADED = 'accounts-loaded'
	# func signature: 
	# IN:	None
	# OUT:	None
	MAIL_CHECK = 'mail-check'
	# func signature: 
	# IN:	new mails, all mails
	# OUT:	None
	MAILS_ADDED = 'mails-added'
	# func signature:
	# IN:	remaining mails
	# OUT:	None
	MAILS_REMOVED = 'mails-removed'
	# func signature:
	# IN:	all mails
	# OUT:	filtered mails
	FILTER_MAILS = 'filter-mails'


#
# Registry class for plugin hooks.
#
# Registered hook functions must not block the mailnag daemon.
# Hook functions with an execution time > 1s should be 
# implemented non-blocking (i. e. asynchronously).
class HookRegistry:
	def __init__(self) -> None:
		self._hooks: dict[HookTypes, list[tuple[int, Callable]]] = {
			HookTypes.ACCOUNTS_LOADED	: [],
			HookTypes.MAIL_CHECK		: [],
			HookTypes.MAILS_ADDED		: [],
			HookTypes.MAILS_REMOVED		: [],
			HookTypes.FILTER_MAILS 		: []
		}
	
	# Priority should be an integer value fom 0 (very high) to 100 (very low)
	# Plugin hooks will be called in order from high to low priority.
	def register_hook_func(
		self,
		hooktype: HookTypes,
		func: Callable,
		priority: int = 100
	) -> None:
		self._hooks[hooktype].append((priority, func))
	
	
	def unregister_hook_func(self, hooktype: HookTypes, func: Callable) -> None:
		pairs = self._hooks[hooktype]
		pair = next(pa for pa in pairs if (pa[1] == func))
		pairs.remove(pair)
	
	
	def get_hook_funcs(self, hooktype: HookTypes) -> list[Callable]:
		pairs_by_prio = sorted(self._hooks[hooktype], key = lambda p: p[0])
		funcs = [f for p, f in pairs_by_prio]
		return funcs


# Abstract base class for a MailnagController instance 
# passed to plugins.
class MailnagController(ABC):
	# Returns a HookRegistry object.
	@abstractmethod
	def get_hooks(self) -> HookRegistry:
		pass
	# Shuts down the Mailnag process.
	# May throw an InvalidOperationException.
	@abstractmethod
	def shutdown(self) -> None:
		pass
	# Enforces a manual mail check.
	# May throw an InvalidOperationException.
	@abstractmethod
	def check_for_mails(self) -> None:
		pass
	# Marks the mail with specified mail_id as read.
	# May throw an InvalidOperationException.
	@abstractmethod
	def mark_mail_as_read(self, mail_id: str) -> None:
		pass


#
# Mailnag Plugin base class
#
class Plugin:
	def __init__(self) -> None:
		# Plugins shouldn't do anything in the constructor. 
		# They are expected to start living if they are actually 
		# enabled (i.e. in the enable() method).
		# Plugin data isn't enabled yet and call to methods like
		# get_mailnag_controller() or get_config().
		pass
	
	#
	# Abstract methods, 
	# to be overriden by derived plugin types.
	#
	def enable(self) -> None:
		# Plugins are expected to
		# register all hooks here.
		raise NotImplementedError
	
	
	def disable(self) -> None:
		# Plugins are expected to
		# unregister all hooks here, 
		# free all allocated resources, 
		# and terminate threads (if any).
		raise NotImplementedError
	
	
	def get_manifest(self) -> tuple[str, str, str, str]:
		# Plugins are expected to
		# return a tuple of the following form:
		# (name, description, version, author).
		raise NotImplementedError
	
	
	def get_default_config(self) -> dict[str, Any]:
		# Plugins are expected to return a
		# dictionary with default values.
		raise NotImplementedError
	
	
	def has_config_ui(self) -> bool:
		# Plugins are expected to return True if
		# they provide a configuration widget,
		# otherwise they must return False.
		raise NotImplementedError
	
	
	def get_config_ui(self) -> Optional[Gtk.Widget]:
		# Plugins are expected to
		# return a GTK widget here.
		# Return None if the plugin 
		# does not need a config widget.
		raise NotImplementedError

	
	def load_ui_from_config(self, config_ui: Gtk.Widget) -> None:
		# Plugins are expected to
		# load their config values (get_config()) 
		# in the widget returned by get_config_ui().
		raise NotImplementedError
	
	
	def save_ui_to_config(self, config_ui: Gtk.Widget) -> None:
		# Plugins are expected to
		# save the config values of the widget
		# returned by get_config_ui() to their config
		# (get_config()).
		raise NotImplementedError
	
	
	#
	# Public methods
	#
	def init(
		self,
		modname: str,
		cfg: RawConfigParser,
		mailnag_controller: Optional[MailnagController]
	) -> None:
		config = {}
		
		# try to load plugin config
		if cfg.has_section(modname):
			for name, value in cfg.items(modname):
				config[name] = value
		
		# sync with default config
		default_config = self.get_default_config()
		for k, v in default_config.items():
			if k not in config:
				config[k] = v
		
		self._modname = modname
		self._config = config
		self._mailnag_controller = mailnag_controller
	
	
	def get_name(self) -> str:
		name = self.get_manifest()[0]
		return name
	
	
	def get_modname(self) -> str:
		return self._modname
	
	
	def get_config(self) -> dict[str, Any]:
		return self._config
	
	
	#
	# Protected methods
	#
	def get_mailnag_controller(self) -> MailnagController:
		assert self._mailnag_controller is not None, "Plugin is not initialized with valid MailnagController"
		return self._mailnag_controller
	
	
	#
	# Static methods
	#
	
	# Note : Plugin instances do not own 
	# a reference to MailnagController object 
	# when instantiated in *config mode*.
	@staticmethod
	def load_plugins(
		cfg: RawConfigParser,
		mailnag_controller: Optional[MailnagController] = None,
		filter_names: Optional[list[str]] = None
	) -> list["Plugin"]:
		plugins = []
		plugin_types = Plugin._load_plugin_types()
		
		for modname, t in plugin_types:			
			try:
				if (filter_names is None) or (modname in filter_names):
					p = t()
					p.init(modname, cfg, mailnag_controller)
					plugins.append(p)
			except:
				logging.exception("Failed to instantiate plugin '%s'" % modname)
		
		return plugins
	
	
	@staticmethod
	def _load_plugin_types() -> list[tuple[str, type["Plugin"]]]:
		plugin_types = []
		
		for path in get_plugin_paths():
			if not path.is_dir():
				continue
			
			for f in path.iterdir():
				mod = None
				modname, ext = os.path.splitext(f.name)
				filename = str(path / f.name)
				
				try:
					if ext.lower() == '.py':
						loader: importlib.abc.SourceLoader = importlib.machinery.SourceFileLoader(modname, filename)
					elif ext.lower() == '.pyc':
						loader = importlib.machinery.SourcelessFileLoader(modname, filename)
					else:
						continue

					spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)

					if spec is None:
						continue

					mod = importlib.util.module_from_spec(spec)
					loader.exec_module(mod)

					for attr_name in dir(mod):
						attr = getattr(mod, attr_name)
						if not inspect.isclass(attr):
							continue
						if issubclass(attr, Plugin) and attr != Plugin:
							plugin_types.append((modname, attr))
				except:
					logging.exception("Error while opening plugin file '%s'" % f)
		
		return plugin_types
