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
from enum import Enum

class BuildStatus(Enum):
    active       = (1, "ubuntuone-client-updating", "Updating the build status...")
    failing      = (2, "ubuntuone-client-error",    "The latest build has failed.")
    not_existing = (3, "ubuntuone-client-offline",  "No latest build status has been found.")
    unknown      = (4, "ubuntuone-client-paused",   "The latest build status is unknown.")
    passing      = (5, "ubuntuone-client-idle",     "The latest build has passed.")

    def __init__(self, number, icon_name, description):
        self.icon_name = icon_name
        self.description = description
        self._value_ = number

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def set_indicator_icon(self, indicator):
        GObject.idle_add(lambda: indicator.set_icon(self.icon_name))

    def set_icon_name(self, gtk_object):
        GObject.idle_add(lambda: gtk_object.set_from_icon_name(self.icon_name, Gtk.IconSize.MENU))

    def set_menu_item_icon(self, menu_item):
        img = Gtk.Image.new_from_icon_name(self.icon_name, Gtk.IconSize.MENU)
        GObject.idle_add(lambda: menu_item.set_image(img))

    def set_text(self, gtk_object):
        GObject.idle_add(lambda: gtk_object.set_text(self.description))

    def __str__(self):
        return self.name
