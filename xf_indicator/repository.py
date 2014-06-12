# -*- coding: utf-8 -*-
"""
    Travis-XF
    ~~~~~~~~~

    Travis-XF Travis CI extreme feedback in form of an ubuntu app-indicator.

    :copyright: (c) 2014 by Frederic Branczyk.
    :license: MIT, see LICENSE for more details.
"""

import json, requests
import webbrowser
from build_status import BuildStatus
from repository_list_box_row import RepositoryListBoxRow
from repository_menu_item import RepositoryMenuItem

class Repository(object):
    travis_base_api_url = "https://api.travis-ci.org/repos/"
    travis_base_url = "https://travis-ci.org/"
    
    def __init__(self, slug):
        self.slug = slug

    def build_status(self):
        print "status: " + self.slug
        try:
            response = requests.get(Repository.travis_base_api_url + self.slug)
            if response.status_code == requests.codes.not_found:
                status = BuildStatus.not_existing
                status.set_menu_item_icon(self.menu_item)
                return status
            json_response = json.loads(response.content)
            if not json_response:
                status = BuildStatus.not_existing
                status.set_menu_item_icon(self.menu_item)
                return status
            if json_response["last_build_result"] == 0:
                status = BuildStatus.passing
                status.set_menu_item_icon(self.menu_item)
                return status
            if json_response["last_build_result"] == None:
                status = BuildStatus.unknown
                status.set_menu_item_icon(self.menu_item)
                return status
            status = BuildStatus.failed
            status.set_menu_item_icon(self.menu_item)
        except ConnectionError:
            print "A connection error occured. Let's try again next cycle."
            status = BuildStatus.active
        return status

    def open_in_webbrowser(self, widget):
        webbrowser.open(Repository.travis_base_url + self.slug)

    def add_menu_item(self, menu):
        self.menu_item = RepositoryMenuItem.factory(self.slug, self.open_in_webbrowser)
        menu.append(self.menu_item)

    def add_to_listbox(self, listbox, remove_callback):
        listbox.add(RepositoryListBoxRow.factory(self, self.slug, remove_callback))
