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

from build_status import BuildStatus
import yaml
import os

CONFIG_FILE=os.path.expanduser("~/.xf-indicator.yaml")

class RepositoryList(object):
    def load(self):
        try:
            f = open(CONFIG_FILE, 'r')
        except IOError:
            print "Config file not found."
        else:
            self.repositories = yaml.load(f)
            f.close()

    def save(self):
        try:
            print "Saving config to " + CONFIG_FILE
            f = open(CONFIG_FILE, 'w')
        except IOError:
            print "Could not save config."
        else:
            yaml.dump(self.repositories, f)
            f.close()

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