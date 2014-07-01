# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2014 Frederic Branczyk fbranczyk@gmail.com
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
### END LICENSE

# This is your preferences window.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.xf-indicator.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from gi.repository import Gio # pylint: disable=E0611

from locale import gettext as _

import logging
logger = logging.getLogger('xf_indicator')

from xf_indicator_lib.NewBuildWindow import NewBuildWindow
from gi.repository import Gtk

class NewBuildXfIndicatorWindow(NewBuildWindow):
    __gtype_name__ = "NewBuildXfIndicatorWindow"
    _instance = None

    @classmethod
    def instance(self):
        if NewBuildXfIndicatorWindow._instance is None:
            NewBuildXfIndicatorWindow._instance = NewBuildXfIndicatorWindow()
        return NewBuildXfIndicatorWindow._instance

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the new build window"""
        super(NewBuildXfIndicatorWindow, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

        self.buildServerCombobox = builder.get_object("buildServerCombobox")

        self.connect("delete-event", self.quit)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()

    def quit(self, window, event):
        window.hide()
        return True

    def set_build_servers(self, build_servers):
        build_server_store = Gtk.ListStore(str)
        #all_builds = []
        #build_servers.iterate(lambda build_server: all_builds.append(str(build_server)))
        #print all_builds
        build_servers.iterate(lambda build_server: build_server_store.append([str(build_server)]))
        self.buildServerCombobox.set_model(model=build_server_store)
        renderer_text = Gtk.CellRendererText()
        self.buildServerCombobox.pack_start(renderer_text, True)
        self.buildServerCombobox.add_attribute(renderer_text, "text", 0)
