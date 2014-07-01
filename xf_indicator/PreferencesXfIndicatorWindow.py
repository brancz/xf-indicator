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

from xf_indicator_lib.PreferencesWindow import PreferencesWindow
from NewBuildXfIndicatorWindow import NewBuildXfIndicatorWindow
from gi.repository import Gtk

class PreferencesXfIndicatorWindow(PreferencesWindow):
    __gtype_name__ = "PreferencesXfIndicatorWindow"
    _instance = None

    @classmethod
    def instance(self):
        if PreferencesXfIndicatorWindow._instance is None:
            PreferencesXfIndicatorWindow._instance = PreferencesXfIndicatorWindow()
        return PreferencesXfIndicatorWindow._instance

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the preferences window"""
        super(PreferencesXfIndicatorWindow, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

        self.buildTreeview = builder.get_object("buildStatusTreeview")
        builder.get_object("addBuildButton").connect("clicked", self.on_add_project)
        builder.get_object("removeBuildButton").connect("clicked", self.on_remove_project)

        self.buildServerTreeview = builder.get_object("buildServerTreeview")

        self.connect("delete-event", self.quit)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.generalSettingsBox = builder.get_object("generalSettingsBox")

        self.show_all()

    def quit(self, window, event):
        self.return_from_preferences_callback(self.projects, self.build_servers)
        window.hide()
        return True

    def on_add_project(self, widget):
        new_build_window = NewBuildXfIndicatorWindow()
        new_build_window.set_build_servers(self.build_servers)
        new_build_window.present()

    def on_remove_project(self, widget):
        print "remove pressed"

    def set_projects(self, projects):
        self.projects = projects

        #cleanup
        old_column = self.buildTreeview.get_column(0)
        if old_column is not None:
            self.buildTreeview.remove_column(old_column)

        #build column
        build_store = Gtk.ListStore(str)
        self.buildTreeview.set_model(model=build_store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Name', renderer, text=0)
        column.set_sort_column_id(0)
        self.buildTreeview.append_column(column)

        projects.iterate(lambda project: build_store.append([str(project)]))

    def set_build_servers(self, build_servers):
        self.build_servers = build_servers

        #cleanup
        old_column = self.buildServerTreeview.get_column(0)
        if old_column is not None:
            self.buildServerTreeview.remove_column(old_column)

        #build column
        build_server_store = Gtk.ListStore(str)
        self.buildServerTreeview.set_model(model=build_server_store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Name', renderer, text=0)
        column.set_sort_column_id(0)
        self.buildServerTreeview.append_column(column)

        build_servers.iterate(lambda build_server: build_server_store.append([str(build_server)]))

    def set_callback(self, callback):
        self.return_from_preferences_callback = callback

    def on_autostart_switch_activate(self, widget, data=None):
        if self.autostart_switch.get_active():
            if not os.path.exists(autostart_dir):
                os.mkdir(autostart_dir)
            if os.path.isdir(autostart_dir):
                os.symlink(autostart_file, installed_file)
        else:
            os.unlink(installed_file)
