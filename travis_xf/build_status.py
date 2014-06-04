# -*- coding: utf-8 -*-
"""
    Travis-XF
    ~~~~~~~~~

    Travis-XF Travis CI extreme feedback in form of an ubuntu app-indicator.

    :copyright: (c) 2014 by Frederic Branczyk.
    :license: MIT, see LICENSE for more details.
"""

import gtk
import appindicator
from enum import Enum

class BuildStatus(Enum):
    passing      = ("ubuntuone-client-idle")
    failed       = ("ubuntuone-client-error")
    not_existing = ("ubuntuone-client-offline")
    unknown      = ("ubuntuone-client-paused")

    def __init__(self, icon_name):
        self.icon_name = icon_name

    def set_indicator_icon(self, indicator):
        indicator.set_icon(self.icon_name)

    def set_menu_item_icon(self, menu_item):
        img = gtk.image_new_from_icon_name(self.icon_name, gtk.ICON_SIZE_MENU)
        menu_item.set_image(img)
