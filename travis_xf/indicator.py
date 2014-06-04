#!/usr/bin/env python

import sys
import gtk
import appindicator
import requests
from repository import Repository, RepositoryList

PING_FREQUENCY = 10 # seconds

class Indicator:
    def __init__(self):
        self.indicator = appindicator.Indicator("travis-xf",
                                          "ubuntuone-client-idle",
                                          appindicator.CATEGORY_APPLICATION_STATUS)

        self.indicator.set_status(appindicator.STATUS_ACTIVE)

        self.repositories = RepositoryList()
        #self.repositories.addRepository("flower-pot/travis-xf")

        self.menu_setup()
        self.indicator.set_menu(self.menu)

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.repositories.create_menu_items(self.menu)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        self.check_all_build_statuses()
        gtk.timeout_add(PING_FREQUENCY * 1000, self.check_all_build_statuses)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def check_all_build_statuses(self):
        self.repositories.set_indicator_icon(self.indicator)
        return True #returning true keeps the async loop alive
