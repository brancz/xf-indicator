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

    def type(self):
        return self.build_server.type()

    def name(self):
        return self.name

    def set_status(self, new_status):
        if self.status is not new_status: 
            self.status = new_status
            self.notify(new_status)

    def refresh_build_status(self):
        status = self.build_server.latest_status_of(self.name)
        self.set_status(status)
        return status

    def latest_build_url(self):
        return self.build_server.latest_build_url_of(self.name)
