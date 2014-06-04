# -*- coding: utf-8 -*-
"""
    Travis-XF
    ~~~~~~~~~

    Travis-XF Travis CI extreme feedback in form of an ubuntu app-indicator.

    :copyright: (c) 2014 by Frederic Branczyk.
    :license: MIT, see LICENSE for more details.
"""

import json, requests
import gtk
import webbrowser
from build_status import BuildStatus

class Repository:
    travis_base_api_url = "https://api.travis-ci.org/repos/"
    travis_base_url = "https://travis-ci.org/"
    
    def __init__(self, slug):
        self.slug = slug

    def build_status(self):
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
        return status

    def handle_push(self, widget):
        webbrowser.open(Repository.travis_base_url + self.slug)

    def add_menu_item(self, menu):
        self.menu_item = gtk.ImageMenuItem(self.slug)
        self.menu_item.set_always_show_image(True)
        self.menu_item.connect("activate", self.handle_push)
        self.menu_item.show()
        menu.append(self.menu_item)

class RepositoryList:
    def __init__(self):
        self.repositories = []

    def addRepository(self, slug):
        repository = Repository(slug)
        self.repositories.append(repository)

    def status(self):
        build_status = lambda repo: repo.build_status()
        statuses = map(build_status, self.repositories)
        statuses = filter(lambda x: x != BuildStatus.passing, statuses)
        if not statuses:
            return BuildStatus.passing
        statuses = filter(lambda x: x != BuildStatus.unknown, statuses)
        if not statuses:
            return BuildStatus.unknown
        statuses = filter(lambda x: x != BuildStatus.not_existing, statuses)
        if not statuses:
            return BuildStatus.not_existing
        statuses = filter(lambda x: x != BuildStatus.failed, statuses)
        if not statuses:
            return BuildStatus.failed

    def set_indicator_icon(self, indicator):
        self.status().set_indicator_icon(indicator)

    def create_menu_items(self, menu):
        for repository in self.repositories:
            repository.add_menu_item(menu)
