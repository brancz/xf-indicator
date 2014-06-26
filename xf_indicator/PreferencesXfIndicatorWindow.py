# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
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
        self.return_from_preferences_callback(self.projects)
        window.hide()
        return True

    def on_add_project(self, widget):
        print "add pressed"

    def on_remove_project(self, widget):
        print "remove pressed"

    def set_projects(self, projects):
        build_store = Gtk.ListStore(str)
        self.buildTreeview.set_model(model=build_store)
        renderer_1 = Gtk.CellRendererText()        
        column_1 = Gtk.TreeViewColumn('Name', renderer_1, text=0)
        column_1.set_sort_column_id(0)        
        self.buildTreeview.append_column(column_1)

        self.projects = projects
        projects.iterate(lambda project: build_store.append([str(project)]))

    def set_build_servers(self, build_servers):
        build_server_store = Gtk.ListStore(str)
        self.buildServerTreeview.set_model(model=build_server_store)
        renderer_2 = Gtk.CellRendererText()        
        column_2 = Gtk.TreeViewColumn('Name', renderer_2, text=0)
        column_2.set_sort_column_id(0)        
        self.buildServerTreeview.append_column(column_2)

        self.build_servers = build_servers
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
