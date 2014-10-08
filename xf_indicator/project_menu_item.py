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

from gi.repository import GObject, Gtk
from ui_build_status import UiBuildStatus
from build_status import BuildStatus
import webbrowser

class ProjectMenuItem(Gtk.ImageMenuItem):
    def __init__(self, project):
        super(Gtk.ImageMenuItem, self).__init__(str(project))
        self.project = project
        self.project.register_on_status_changed(self)
        self.connect("activate", self.on_project_activate)
        self.set_always_show_image(True)
        self.show()
        UiBuildStatus.by_build_status(BuildStatus.active).set_menu_item_icon(self)

    def on_status_changed(self, subject, new_status):
        ui_build_status = UiBuildStatus.by_build_status(new_status)
        ui_build_status.set_menu_item_icon(self)

    def on_project_activate(self, widget):
        self.open_project_in_webbrowser()

    def open_project_in_webbrowser(self):
        webbrowser.open(self.project.latest_build_url())
