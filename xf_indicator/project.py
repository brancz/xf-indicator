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

import webbrowser
from project_list_box_row import ProjectListBoxRow
from project_menu_item import ProjectMenuItem

class Project(object):
    def __init__(self, name, build_server):
        self.name = name
        self.build_server = build_server

    def add_menu_item(self, menu):
        self.menu_item = ProjectMenuItem.factory(self.name, self.open_in_webbrowser)
        menu.append(self.menu_item)

    def add_to_listbox(self, listbox, remove_callback):
        listbox.add(ProjectListBoxRow.factory(self.name, remove_callback))

    def build_status(self):
        status = self.build_server.latest_status_of(self.name)
        print "status of " + self.name + ": " + str(status)
        status.set_menu_item_icon(self.menu_item)
        return status

    def open_in_webbrowser(self, widget):
        webbrowser.open(self.build_server.latest_build_url_of(self.name))
