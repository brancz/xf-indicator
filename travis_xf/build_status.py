# -*- coding: utf-8 -*-
"""
    Travis-XF
    ~~~~~~~~~

    Travis-XF Travis CI extreme feedback in form of an ubuntu app-indicator.

    :copyright: (c) 2014 by Frederic Branczyk.
    :license: MIT, see LICENSE for more details.
"""

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
