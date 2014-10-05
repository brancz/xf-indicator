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

from xf_indicator_lib.add_project_window import AddProjectWindow
from project import Project
from gi.repository import Gtk

class AddProjectXfIndicatorWindow(AddProjectWindow):
    __gtype_name__ = "AddProjectXfIndicatorWindow"
    _instance = None

    @classmethod
    def instance(self):
        if AddProjectXfIndicatorWindow._instance is None:
            AddProjectXfIndicatorWindow._instance = AddProjectXfIndicatorWindow()
        return AddProjectXfIndicatorWindow._instance

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the new build window"""
        super(AddProjectXfIndicatorWindow, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

        self.build_server_combobox = builder.get_object("buildServerCombobox")
        self.project_name_entry = builder.get_object("projectNameEntry")
        self.project_name_entry.connect("activate", self.on_enter_pressed)
        self.add_project_button = builder.get_object("addProjectButton")
        self.add_project_button.connect("clicked", self.on_add_project_button_activate)

        self.connect("delete-event", self.quit)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()

    def quit(self, window, event):
        window.hide()
        return True

    def on_enter_pressed(self, widget):
        self.add_and_hide()

    def on_add_project_button_activate(self, widget):
        self.add_and_hide()
    
    def add_and_hide(self):
        project_name = self.project_name_entry.get_text()
        if not project_name:
            # please provide a build-name
            return
        project_build_server_index = self.build_server_combobox.get_active()
        if project_build_server_index is -1:
            # please select a build-server
            return
        project_build_server = self.build_servers.get(project_build_server_index)
        project = Project(project_name, project_build_server)
        self.add_callback(project)
        self.hide()

    def set_add_callback(self, callback):
        self.add_callback = callback

    def set_build_servers(self, build_servers):
        self.build_servers = build_servers
        build_server_store = Gtk.ListStore(str)
        for build_server in build_servers:
            build_server_store.append([str(build_server)])
        self.build_server_combobox.set_model(model=build_server_store)
        renderer_text = Gtk.CellRendererText()
        self.build_server_combobox.pack_start(renderer_text, True)
        self.build_server_combobox.add_attribute(renderer_text, "text", 0)
