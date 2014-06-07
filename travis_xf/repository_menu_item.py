# -*- coding: utf-8 -*-
"""
    Travis-XF
    ~~~~~~~~~

    Travis-XF Travis CI extreme feedback in form of an ubuntu app-indicator.

    :copyright: (c) 2014 by Frederic Branczyk.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import generators
from gi.repository import GObject, Gtk

class RepositoryMenuItem(object):
    def factory(slug, activate_callback):
        menu_item = Gtk.ImageMenuItem(slug)
        menu_item.set_always_show_image(True)
        menu_item.connect("activate", activate_callback)
        menu_item.show()
        return menu_item
    factory = staticmethod(factory)
