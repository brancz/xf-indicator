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

from project_list import ProjectList
from build_server_list import BuildServerList
from preferences_window import PreferencesWindow
from build_status import BuildStatus
from timer_with_resume import TimerWithResume
from XfIndicatorHelpDialog import XfIndicatorHelpDialog
from PreferencesXfIndicatorWindow import PreferencesXfIndicatorWindow
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

        self.projects = ProjectList()
        self.projects.register_on_status_changed(self)
        self.build_servers = BuildServerList()

        self.indicator.set_menu(self.build_menu())

        self.setup_refresh_timer()

    def on_status_changed(self, new_status):
        new_status.set_indicator_icon(self.indicator)

    def on_preferences_activate(self, widget):
        preferences_window = PreferencesXfIndicatorWindow.instance()
        preferences_window.set_projects(self.projects)
        preferences_window.set_build_servers(self.build_servers)
        preferences_window.set_callback(self.return_from_preferences_callback)
        preferences_window.present()
        self.refresh_timer.stop()

    def on_help_activate(self, widget):
        help_dialog = XfIndicatorHelpDialog.instance()
        help_dialog.present()

    def return_from_preferences_callback(self, new_projects, new_build_servers):
        # set new project list and reset connected components
        self.new_projects = new_projects
        self.build_servers = new_build_servers
        self.indicator.set_menu(self.build_menu())
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

    def setup_refresh_timer(self):
        self.refresh_timer = TimerWithResume(lambda: self.refresh_loop())
        self.refresh_timer.start()

    def refresh_loop(self):
        self.projects.refresh_build_status()

    def quit(self, widget):
        Gtk.main_quit()
