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

from status_subject import StatusSubject
from build_status import BuildStatus
from sets import Set

class ProjectList(StatusSubject):

    def __init__(self, shelf=None):
        self.projects = Set()
        if shelf is not None and shelf.has_key("project_list"):
            self.projects = shelf["project_list"]
        self.status = None

    def __iter__(self):
        return self.projects.__iter__()

    def add(self, project):
        self.projects.add(project)

    def save(self, shelf):
        shelf["project_list"] = self.projects

    def remove(self, project):
        self.projects.remove(project)

    def build_status(self):
        statuses = map(lambda project: project.build_status(), self.projects)
        try:
            # the worst status is the smallest one
            status = min(statuses)
        except ValueError:
            # occurs when statuses is empty, thus don't show an error
            status = BuildStatus.passing
        if self.status is not status:
            self.status = status
            self.notify(status)
        return self.status

class Project(StatusSubject):
    def __init__(self, name, build_server):
        self.name = name
        self.build_server = build_server
        self.status = None

    def __eq__(self, other):
        return type(other) == Project and self.name == other.name and self.build_server == other.build_server

    def __hash__(self):
        return hash(self.name + str(hash(self.build_server)))

    def __str__(self):
        return self.name

    def build_server_name(self):
        return str(self.build_server)

    def set_status(self, new_status):
        if self.status is not new_status: 
            self.status = new_status
            self.notify(new_status)

    def build_status(self):
        status = self.build_server.latest_status_of(self.name)
        print "{0}: {1}".format(self, status)
        self.set_status(status)
        return status

    def latest_build_url(self):
        return self.build_server.latest_build_url_of(self.name)

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['observers']
        return odict
