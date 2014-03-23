# encoding: utf-8

# Nagstamon - Nagios status monitor for your desktop
# Copyright (C) 2008-2013 Henri Wahl <h.wahl@ifw-dresden.de> et al.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
import sys
import socket

from Nagstamon.Server.Generic import GenericServer
from websocket import create_connection, WebSocketConnectionClosedException


class NagiosServer(GenericServer):
    """
        object of Nagios server - when nagstamon will be able to poll various servers this
        will be useful
        As Nagios is the default server type all its methods are in GenericServer
    """

    TYPE = 'Nagios'

    # autologin is used only by Centreon
    DISABLED_CONTROLS = ["input_checkbutton_use_autologin", "label_autologin_key", "input_entry_autologin_key"]
    ENABLED_CONTROLS = ["label_monitor_websocket_url", "input_entry_websocket_url"]

    def __init__(self, **kwds):
        GenericServer.__init__(self, **kwds)

        self.ws = None

    def Debug(self, *args, **kwargs):
        if str(self.conf.debug_mode) == "True":
            GenericServer.Debug(self, *args, **kwargs)

    def websocket_init(self):
        self.Debug(server=self.get_name(), debug="Websocket: Connecting to %s..." % self.websocket_url)

        try:
            self.ws = create_connection(self.websocket_url)
            return True
        except socket.error:
            self.ws = None

        return False

    def websocket_wait(self):
        if not self.ws and not self.websocket_init():
            return False

        try:
            self.Debug(server=self.get_name(), debug="Websocket: waiting for an event...")
            self.ws.recv()
            self.Debug(server=self.get_name(), debug="Websocket: event received!")
            return True
        except WebSocketConnectionClosedException:
            self.Debug(server=self.get_name(), debug="Websocket: broken connection")
            self.websocket_init()

        return False
