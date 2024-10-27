# test_soundplugin.py
#
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

"""Test cases for sound plugin."""

import pytest

import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gst
from Mailnag.common.plugins import (
    Plugin,
    HookRegistry,
    HookTypes,
    MailnagController,
)

import configparser
from unittest.mock import MagicMock, patch, call, ANY
import sys
import time


@pytest.fixture
def fake_gst():
    with patch.object(gi.repository, "Gst", autospec=Gst) as fake:
        yield fake


class SampleController(MailnagController):
    def __init__(self):
        self.hooks = HookRegistry()

    def get_hooks(self):
        return self.hooks


def get_soundplugin(controller):
    config = configparser.ConfigParser()
    plugins = Plugin.load_plugins(config, controller, 'soundplugin')
    soundplugin = plugins[0]
    return soundplugin


def test_create_plugin():
    # GIVEN
    controller = SampleController()
    config = configparser.ConfigParser()
    # WHEN
    plugins = Plugin.load_plugins(config, controller, 'soundplugin')
    assert len(plugins) == 1
    soundplugin = plugins[0]
    # THEN
    assert soundplugin


def test_enable_should_register_a_hook():
    # GIVEN
    controller = SampleController()
    soundplugin = get_soundplugin(controller)

    # WHEN
    soundplugin.enable()

    # THEN
    hook_funcs = controller.hooks.get_hook_funcs(HookTypes.MAILS_ADDED)
    assert len(hook_funcs) == 1


def test_mails_added_should_initialize_gst(fake_gst):
    # GIVEN
    controller = SampleController()
    soundplugin = get_soundplugin(controller)
    soundplugin.enable()

    # WHEN
    hook_func = controller.hooks.get_hook_funcs(HookTypes.MAILS_ADDED)[0]
    hook_func([], [])

    # THEN
    fake_gst.init.assert_called_once_with(None)


def test_multiple_mails_added_should_initialize_gst_only_once(fake_gst):
    # GIVEN
    controller = SampleController()
    soundplugin = get_soundplugin(controller)
    soundplugin.enable()

    # WHEN
    hook_func = controller.hooks.get_hook_funcs(HookTypes.MAILS_ADDED)[0]
    hook_func([], [])
    hook_func([], [])

    # THEN
    fake_gst.init.assert_called_once_with(None)


@pytest.mark.xfail(reason='Sound plugin uses wrong uri in venvs.')
def test_mails_added_should_play_correct_sound(fake_gst):
    # GIVEN
    play = MagicMock()
    factory = MagicMock()
    fake_gst.ElementFactory = factory
    factory.make.return_value = play
    controller = SampleController()
    soundplugin = get_soundplugin(controller)
    soundplugin.enable()

    # WHEN
    hook_func = controller.hooks.get_hook_funcs(HookTypes.MAILS_ADDED)[0]
    hook_func([], [])

    # THEN
    play.set_property.assert_called_once_with('uri', ANY)
    args = play.set_property.call_args.args
    assert args[1] == 'file://' + sys.prefix + '/share/mailnagger/mailnag.ogg'


def test_mails_added_should_start_playing_sound(fake_gst):
    # GIVEN
    factory = MagicMock()
    fake_gst.ElementFactory = factory
    play = MagicMock()
    factory.make.return_value = play
    bus = MagicMock()
    play.get_bus.return_value = bus

    controller = SampleController()
    soundplugin = get_soundplugin(controller)
    soundplugin.enable()

    # WHEN
    hook_func = controller.hooks.get_hook_funcs(HookTypes.MAILS_ADDED)[0]
    hook_func([], [])

    # THEN
    play.set_state.assert_called_with(fake_gst.State.PLAYING)


def test_end_of_stream_stop_playing(fake_gst):
    # GIVEN
    factory = MagicMock()
    fake_gst.ElementFactory = factory
    play = MagicMock()
    factory.make.return_value = play
    bus = MagicMock()
    play.get_bus.return_value = bus

    controller = SampleController()
    soundplugin = get_soundplugin(controller)
    soundplugin.enable()
    hook_func = controller.hooks.get_hook_funcs(HookTypes.MAILS_ADDED)[0]
    hook_func([], [])

    # WHEN
    args = bus.connect.call_args.args
    eos_callback = args[1]
    eos_callback(bus, "End of stream")

    # THEN
    play.set_state.assert_called_with(fake_gst.State.NULL)

