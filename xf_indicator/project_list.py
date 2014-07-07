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
from status_subject import StatusSubject
import yaml
import os

#CONFIG_FILE=os.path.expanduser("~/.xf-indicator.yaml")

class ProjectList(StatusSubject):

    def __init__(self):
        self.projects = []
        self.status = None

    def __iter__(self):
        return self.projects.__iter__()

    def add_project(self, project):
        self.projects.append(project)

    def refresh_build_status(self):
        extract_build_status = lambda project: project.refresh_build_status()
        statuses = map(extract_build_status, self.projects)
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
