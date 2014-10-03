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
from build_server import BuildServer

from locale import gettext as _

import logging
logger = logging.getLogger('xf_indicator')

from xf_indicator_lib.new_build_server_window import NewBuildServerWindow
from project import Project
from build_server_builder import JenkinsServerBuilder, TravisCIEnterpriseServerBuilder, TravisCIComBuilder
from gi.repository import Gtk, GObject

class NewBuildServerXfIndicatorWindow(NewBuildServerWindow):
    __gtype_name__ = "NewBuildServerXfIndicatorWindow"
    _instance = None

    @classmethod
    def instance(self):
        if NewBuildServerXfIndicatorWindow._instance is None:
            NewBuildServerXfIndicatorWindow._instance = NewBuildServerXfIndicatorWindow()
        return NewBuildServerXfIndicatorWindow._instance

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the new build window"""
        super(NewBuildServerXfIndicatorWindow, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

        self.main_list_box = builder.get_object("newBuildServerBox")

        self.build_server_type_combobox = builder.get_object("buildServerTypeCombobox")

        self.build_server_type_store = Gtk.ListStore(str)

        self.build_server_type_to_builder = {
            "Travis CI Pro": TravisCIComBuilder,
            "Travis CI Enterprise": TravisCIEnterpriseServerBuilder,
            "Jenkins": JenkinsServerBuilder
        }

        for build_server_type in self.build_server_type_to_builder:
            self.build_server_type_store.append([build_server_type])

        self.build_server_type_combobox.set_model(model=self.build_server_type_store)

        renderer_text = Gtk.CellRendererText()

        self.build_server_type_combobox.pack_start(renderer_text, True)
        self.build_server_type_combobox.add_attribute(renderer_text, "text", 0)
        self.build_server_type_combobox.connect("changed", self.on_build_server_type_changed)

        self.connect("delete-event", self.quit)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()

    def on_build_server_type_changed(self, widget):
        iter = self.build_server_type_combobox.get_active_iter()
        type = self.build_server_type_combobox.get_model().get_value(iter, 0)
        if(hasattr(self, 'server_builder')):
            self.server_builder.remove()
        if(hasattr(self, 'add_row')):
            self.main_list_box.remove(self.add_row)
        self.server_builder = self.build_server_type_to_builder[type](self.main_list_box)
        self.server_builder.add_form()

        self.add_row =Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        add_button = Gtk.Button("ADD")
        add_button.connect("clicked", self.on_add)
        self.add_row.pack_start(add_button, True, True, 0)

        self.main_list_box.add(self.add_row)

        self.show_all()

    def on_add(self, widget):
        try:
            build_server = self.server_builder.build()
            self.add_callback(build_server)
            self.hide()
        except ValueError as e:
            Gtk.MessageDialog(text=str(e), parent=self).show_all()

    def quit(self, window, event):
        window.hide()
        return True

    def on_enter_pressed(self, widget):
        self.on_add(None)

    def set_callback(self, callback):
        self.add_callback = callback
