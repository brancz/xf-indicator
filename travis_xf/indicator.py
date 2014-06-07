#!/usr/bin/env python

import requests
import sys
import threading

from repository import Repository
from repository_list import RepositoryList
from preferences_window import PreferencesWindow
from build_status import BuildStatus
from gi.repository import AppIndicator3
from gi.repository import GObject, Gtk, GLib

REFRESH_INTERVAL = 10

class Indicator:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new("travis-xf",
                                          "ubuntuone-client-idle",
                                          AppIndicator3.IndicatorCategory.APPLICATION_STATUS)

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.repositories = RepositoryList()
        self.repositories.add_repository(Repository("openpizza/openpizza"))

        self.indicator.set_menu(self.build_menu())

    def on_preferences_activate(self, widget):
        self.preferences_window = PreferencesWindow(self.repositories, self.return_from_preferences_callback)

    def return_from_preferences_callback(self, new_repositories):
        # set new repositories and reset connected components
        self.repositories = new_repositories
        self.indicator.set_menu(self.build_menu())
        self.reset_refresh_timer()

    def build_menu(self):
        menu = Gtk.Menu()

        self.repositories.create_menu_items(menu)
        self.add_menu_item(menu, "Preferences", self.on_preferences_activate)
        self.add_menu_item(menu, "Quit", self.quit)

        return menu

    def add_menu_item(self, menu, title, activate_handler):
        item = Gtk.MenuItem(title)
        item.connect("activate", activate_handler)
        item.show()
        menu.append(item)

    def setup_refresh_timer(self):
        # we want to execute immediately and then start the cycle
        BuildStatus.active.set_indicator_icon(self.indicator)
        self.refresh_timer = threading.Timer(REFRESH_INTERVAL, self.check_all_build_statuses)
        self.refresh_timer.start()

    def reset_refresh_timer(self):
        self.refresh_timer.cancel()
        self.setup_refresh_timer()

    def check_all_build_statuses(self):
        self.repositories.set_indicator_icon(self.indicator)

    def main(self):
        self.setup_refresh_timer()
        Gtk.main()

    def quit(self, widget):
        sys.exit(0)
