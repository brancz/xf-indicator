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

import os
from gi.repository import Gtk, GLib, Gio
from project import Project
from build_server import TravisCIOrg
from xf_indicator_lib.helpers import get_media_file

autostart_dir = os.path.join(GLib.get_user_config_dir(),"autostart/")
autostart_template = "xf-indicator-autostart.desktop"
autostart_file = get_media_file(autostart_template)
autostart_file = autostart_file.replace("file:///", '')
installed_file = os.path.join(autostart_dir, autostart_template)

class PreferencesWindow(Gtk.Window):

    def __init__(self, projects, return_from_preferences_callback):
        self.return_from_preferences_callback = return_from_preferences_callback

        Gtk.Window.__init__(self, title="Preferences")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        self.superlistbox = Gtk.ListBox()
        self.superlistbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hbox.pack_start(self.superlistbox, True, True, 0)

        ###
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hbox.pack_start(self.listbox, True, True, 0)
        row.add(hbox)

        ###
        self.add_autostart_switch()

        #only work on a copy of the project list until closing the preferences,
        #thus sumbmitting the change
        self.projects = projects.clone()
        self.projects.add_all_to_listbox(self.listbox)

        self.superlistbox.add(row)

        ###
        self.add_add_project_button()

        self.connect("delete-event", self.quit)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.show_all()

    def quit(self, window, event):
        self.return_from_preferences_callback(self.projects)

    def add_project(self, widget):
        project_entry_text = self.entry.get_text()
        if project_entry_text != "":
            project = Project(project_entry_text, TravisCIOrg())
            project.add_to_listbox(self.listbox, self.projects.remove_from_listbox_callback)
            self.projects.add(project)
            self.entry.set_text("")

    def add_add_project_button(self):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.entry = Gtk.Entry(xalign=0)
        self.entry.connect("activate", self.add_project)
        self.entry.set_placeholder_text("e.g. twbs/bootstrap")
        add_button = Gtk.Button("Add")
        add_button.connect("clicked", self.add_project)
        hbox.pack_start(self.entry, True, True, 0)
        hbox.pack_start(add_button, False, True, 0)

        self.superlistbox.add(row)

    def add_autostart_switch(self):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        autostart_label = Gtk.Label("Autostart?", xalign=0)
        self.autostart_switch = Gtk.Switch()
        if os.path.isfile(installed_file):
            self.autostart_switch.set_active(True)
        self.autostart_switch.connect('notify::active', self.on_autostart_switch_activate)
        hbox.pack_start(autostart_label, True, True, 0)
        hbox.pack_start(self.autostart_switch, False, True, 0)

        self.superlistbox.add(row)
        separator = Gtk.HSeparator()
        separator.set_margin_bottom(5)
        separator.set_margin_top(5)
        self.superlistbox.add(separator)

    def on_autostart_switch_activate(self, widget, data=None):
        if self.autostart_switch.get_active():
            if not os.path.exists(autostart_dir):
                os.mkdir(autostart_dir)
            if os.path.isdir(autostart_dir):
                os.symlink(autostart_file, installed_file)
        else:
            os.unlink(installed_file)
