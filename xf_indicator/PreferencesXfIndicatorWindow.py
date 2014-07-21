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

from gi.repository import Gio, GLib # pylint: disable=E0611

from locale import gettext as _

import logging
logger = logging.getLogger('xf_indicator')

import os

from xf_indicator_lib.PreferencesWindow import PreferencesWindow
from NewBuildXfIndicatorWindow import NewBuildXfIndicatorWindow
from NewBuildServerXfIndicatorWindow import NewBuildServerXfIndicatorWindow
from gi.repository import Gtk, GObject, GdkPixbuf
from xf_indicator_lib.helpers import get_media_file

autostart_dir = os.path.join(GLib.get_user_config_dir(),"autostart/")
autostart_template = "xf-indicator-autostart.desktop"
autostart_file = get_media_file(autostart_template)
autostart_file = autostart_file.replace("file:///", '')
installed_file = os.path.join(autostart_dir, autostart_template)

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
        builder.get_object("addBuildServerButton").connect("clicked", self.on_add_build_server)
        builder.get_object("removeBuildServerButton").connect("clicked", self.on_remove_build_server)

        self.connect("delete-event", self.quit)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.generalSettingsBox = builder.get_object("generalSettingsBox")
        self.autostart_switch = builder.get_object("autostartSwitch")
        self.autostart_switch.connect("notify::active", self.on_autostart_switch_activate)
        if os.path.isfile(installed_file):
            self.autostart_switch.set_active(True)

        self.show_all()

    def quit(self, window, event):
        self.return_from_preferences_callback(self.projects, self.build_servers)
        window.hide()
        return True

    def on_add_project(self, widget):
        new_build_window = NewBuildXfIndicatorWindow()
        new_build_window.set_build_servers(self.build_servers)
        new_build_window.set_add_callback(self.new_build_callback)
        new_build_window.present()

    def new_build_callback(self, project):
        self.projects.add(project)
        self.set_projects(self.projects)

    def on_remove_project(self, widget):
        (model, pathlist) = self.buildTreeview.get_selection().get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            project = model.get_value(tree_iter, 0)
            self.projects.remove(project)
            self.set_projects(self.projects)

    def set_projects(self, projects):
        self.projects = projects

        #cleanup
        old_columns = self.buildTreeview.get_columns()
        for column in old_columns:
            self.buildTreeview.remove_column(column)

        build_store = Gtk.ListStore(GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT)

        self.buildTreeview.set_model(model=build_store)

        #build server type column
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Build Server', renderer, text=0)
        column.set_sort_column_id(0)
        def extract_project_type(column, cell, model, iter, user_data):
            build_server_name = model.get_value(iter, 0).build_server_name()
            cell.props.text = build_server_name
        column.set_cell_data_func(renderer, extract_project_type)
        self.buildTreeview.append_column(column)

        #build column
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Name', renderer, text=1)
        column.set_sort_column_id(1)
        def extract_project_name(column, cell, model, iter, user_data):
            project = model.get_value(iter, 1)
            cell.props.text = str(project)
        column.set_cell_data_func(renderer, extract_project_name)
        self.buildTreeview.append_column(column)

        for project in projects:
            build_store.append([project, project])

    def on_add_build_server(self, widget):
        build_server_window = NewBuildServerXfIndicatorWindow()
        build_server_window.set_callback(self.new_build_server_callback)
        build_server_window.present()

    def new_build_server_callback(self, new_build_server):
        self.build_servers.add(new_build_server)
        self.set_build_servers(self.build_servers)

    def on_remove_build_server(self, widget):
        (model, pathlist) = self.buildServerTreeview.get_selection().get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            build_server = model.get_value(tree_iter, 0)
            self.build_servers.remove(build_server)
            self.set_build_servers(self.build_servers)

    def set_build_servers(self, build_servers):
        self.build_servers = build_servers

        #cleanup
        old_columns = self.buildServerTreeview.get_columns()
        for column in old_columns:
            self.buildServerTreeview.remove_column(column)

        build_server_store = Gtk.ListStore(GdkPixbuf.Pixbuf, GObject.TYPE_PYOBJECT)
        self.buildServerTreeview.set_model(model=build_server_store)

        #build server type column
        renderer = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn('Type', renderer)
        column.add_attribute(renderer, "pixbuf", 0)
        self.buildServerTreeview.append_column(column)

        #build server name column
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Name', renderer, text=0)
        column.set_sort_column_id(1)
        def extract_build_server_name(column, cell, model, iter, user_data):
            build_server_name = str(model.get_value(iter, 1))
            cell.props.text = build_server_name
        column.set_cell_data_func(renderer, extract_build_server_name)
        self.buildServerTreeview.append_column(column)

        build_server_images = {
            "Travis CI": "../data/media/travis.png",
            "Travis CI Pro": "../data/media/travis.png",
            "Travis CI Enterprise": "../data/media/travis.png",
            "Jenkins": "../data/media/jenkins.png"
        }

        for build_server in build_servers:
            image = GdkPixbuf.Pixbuf.new_from_file(build_server_images[build_server.type()])
            build_server_store.append([image, build_server])

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
