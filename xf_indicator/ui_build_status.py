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

from gi.repository import Gtk, GObject
from build_status import BuildStatus

class UiBuildStatus(object):

    def __init__(self, build_status):
        information = self._information_by_build_status(build_status)
        self.icon_name = information["icon_name"]
        self.description = information["description"]

    def _information_by_build_status(self, build_status):
        information = {
            BuildStatus.active: {
                "icon_name": "ubuntuone-client-updating",
                "description": "Updating the build status..."
            },
            BuildStatus.failing: {
                "icon_name": "ubuntuone-client-error",
                "description": "The latest build has failed."
            },
            BuildStatus.not_existing: {
                "icon_name": "ubuntuone-client-offline",
                "description": "No latest build status has been found."
            },
            BuildStatus.unknown: {
                "icon_name": "ubuntuone-client-paused",
                "description": "The latest build status is unknown."
            },
            BuildStatus.passing: {
                "icon_name": "ubuntuone-client-idle",
                "description": "The latest build has passed."
            }
        }
        return information[build_status]

    def set_indicator_icon(self, indicator):
        GObject.idle_add(lambda: indicator.set_icon(self.icon_name))

    def set_icon_name(self, gtk_object):
        GObject.idle_add(lambda: gtk_object.set_from_icon_name(self.icon_name, Gtk.IconSize.MENU))

    def set_menu_item_icon(self, menu_item):
        img = Gtk.Image.new_from_icon_name(self.icon_name, Gtk.IconSize.MENU)
        GObject.idle_add(lambda: menu_item.set_image(img))

    def set_text(self, gtk_object):
        GObject.idle_add(lambda: gtk_object.set_text(self.description))
