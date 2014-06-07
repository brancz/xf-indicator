# -*- coding: utf-8 -*-
"""
    Travis-XF
    ~~~~~~~~~

    Travis-XF Travis CI extreme feedback in form of an ubuntu app-indicator.

    :copyright: (c) 2014 by Frederic Branczyk.
    :license: MIT, see LICENSE for more details.
"""

from build_status import BuildStatus

class RepositoryList(object):
    def __init__(self):
        self.repositories = []

    def add_repository(self, repository):
        self.repositories.append(repository)

    def status(self):
        build_status = lambda repo: repo.build_status()
        statuses = map(build_status, self.repositories)
        for status in statuses:
            print status
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
