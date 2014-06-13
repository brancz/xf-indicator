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
    passing      = ("ubuntuone-client-idle")
    failed       = ("ubuntuone-client-error")
    not_existing = ("ubuntuone-client-offline")
    unknown      = ("ubuntuone-client-paused")
    active       = ("ubuntuone-client-updating")

    def __init__(self, icon_name):
        self.icon_name = icon_name

    def set_indicator_icon(self, indicator):
        GObject.idle_add(lambda: indicator.set_icon(self.icon_name))

    def set_menu_item_icon(self, menu_item):
        img = Gtk.Image.new_from_icon_name(self.icon_name, Gtk.IconSize.MENU)
        GObject.idle_add(lambda: menu_item.set_image(img))
