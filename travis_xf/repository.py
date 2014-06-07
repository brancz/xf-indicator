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

    def open_in_webbrowser(self, widget):
        webbrowser.open(Repository.travis_base_url + self.slug)

    def add_menu_item(self, menu):
        self.menu_item = RepositoryMenuItem.factory(self.slug, self.open_in_webbrowser)
        menu.append(self.menu_item)

    def add_to_listbox(self, listbox, remove_callback):
        listbox.add(RepositoryListBoxRow.factory(self, self.slug, remove_callback))

class RepositoryList(object):
    def __init__(self):
        self.repositories = []

    def add_repository(self, repository):
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
    
    def add_all_to_listbox(self, listbox):
        for repo in self.repositories:
            repo.add_to_listbox(listbox, self.remove_from_listbox_callback)

    def remove_from_listbox_callback(self, repo):
        self.repositories.remove(repo)
    
    def clone(self):
        clone = RepositoryList()
        for repo in self.repositories:
            clone.add_repository(repo)
        return clone
