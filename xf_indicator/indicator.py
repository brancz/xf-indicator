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

import requests
import sys
import threading
import shelve

from project import ProjectList
from build_server import BuildServerList
from ui_build_status import UiBuildStatus
from timer_with_resume import TimerWithResume
from help_dialog import XfIndicatorHelpDialog
from preferences_window import PreferencesXfIndicatorWindow
from project_menu_item import ProjectMenuItem
from status_subject import StatusSubject
from gi.repository import AppIndicator3
from gi.repository import Gtk

class Indicator(StatusSubject):
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new("xf-indicator",
                                          "ubuntuone-client-idle",
                                          AppIndicator3.IndicatorCategory.APPLICATION_STATUS)

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        shelf = shelve.open("persistence")
        self.projects = ProjectList(shelf)
        self.build_servers = BuildServerList(shelf)
        self.refresh_interval = 10
        if shelf.has_key("refresh_interval"):
            self.refresh_interval = shelf["refresh_interval"]
        shelf.close()

        self.projects.register_on_status_changed(self)
        self.indicator.set_menu(self.build_menu())
        self.refresh_timer = self.setup_refresh_timer(self.refresh_interval)
        self.refresh_timer.start()

    def on_status_changed(self, subject, new_status):
        ui_build_status = UiBuildStatus.by_build_status(new_status)
        ui_build_status.set_indicator_icon(self.indicator)

    def on_preferences_activate(self, widget):
        preferences_window = PreferencesXfIndicatorWindow.instance()
        preferences_window.set_projects(self.projects)
        preferences_window.set_build_servers(self.build_servers)
        preferences_window.set_refresh_interval(self.refresh_interval)
        preferences_window.set_callback(self.return_from_preferences_callback)
        preferences_window.present()
        self.refresh_timer.stop()

    def on_help_activate(self, widget):
        help_dialog = XfIndicatorHelpDialog.instance()
        help_dialog.present()

    def return_from_preferences_callback(self, new_projects, new_build_servers, new_refresh_interval):
        self.new_projects = new_projects
        self.build_servers = new_build_servers
        self.indicator.set_menu(self.build_menu())
        self.refresh_interval = new_refresh_interval
        self.refresh_timer.set_refresh_interval(new_refresh_interval)
        self.refresh_timer.resume()

    def build_menu(self):
        menu = Gtk.Menu()

        for project in self.projects:
            menu.append(ProjectMenuItem(project))

        self.add_menu_item(menu, "Preferences", self.on_preferences_activate)
        self.add_menu_item(menu, "Help", self.on_help_activate)
        self.add_menu_item(menu, "Quit", self.quit)

        return menu

    def add_menu_item(self, menu, title, activate_handler):
        item = Gtk.MenuItem(title)
        item.connect("activate", activate_handler)
        item.show()
        menu.append(item)

    def setup_refresh_timer(self, interval):
        return TimerWithResume(self.projects, interval)

    def quit(self, widget):
        shelf = shelve.open("persistence")
        self.projects.save(shelf)
        self.build_servers.save(shelf)
        shelf["refresh_interval"] = self.refresh_interval
        shelf.close()
        Gtk.main_quit()
