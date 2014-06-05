#!/usr/bin/env python

import requests
import sys

from repository import Repository, RepositoryList
from preferences_window import PreferencesWindow
from build_status import BuildStatus
from gi.repository import AppIndicator3
from gi.repository import GObject, Gtk, GLib

PING_FREQUENCY = 10 # seconds

class Indicator:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new("travis-xf",
                                          "ubuntuone-client-idle",
                                          AppIndicator3.IndicatorCategory.APPLICATION_STATUS)

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.repositories = RepositoryList()
        self.repositories.add_repository(Repository("openpizza/openpizza"))

        self.menu_setup()
        self.indicator.set_menu(self.menu)

    def on_preferences_activate(self, widget):
        self.preferences_window = PreferencesWindow(self.repositories, self.return_from_preferences_callback)
        self.preferences_window.show_all()

    def return_from_preferences_callback(self, new_repositories):
        self.repositories = new_repositories
        BuildStatus.active.set_indicator_icon(self.indicator)
        self.menu_setup()
        self.indicator.set_menu(self.menu)

    def menu_setup(self):
        self.menu = Gtk.Menu()

        self.repositories.create_menu_items(self.menu)

        self.preferences_item = Gtk.MenuItem("Preferences")
        self.preferences_item.connect("activate", self.on_preferences_activate)
        self.preferences_item.show()
        self.menu.append(self.preferences_item)

        self.quit_item = Gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        self.check_all_build_statuses()
        GLib.timeout_add_seconds(PING_FREQUENCY, self.check_all_build_statuses)
        Gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def check_all_build_statuses(self):
        self.repositories.set_indicator_icon(self.indicator)
        return True #returning true keeps the async loop alive
