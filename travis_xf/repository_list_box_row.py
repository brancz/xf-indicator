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

class RepositoryListBoxRow(object):
    def factory(slug, activate_callback):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(slug, xalign=0)
        remove_button = Gtk.Button("Remove")
        remove_button.connect("clicked", activate_callback)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(remove_button, False, True, 0)

        #show all of them
        hbox.show()
        row.show()
        label.show()
        remove_button.show()

        return row
    factory = staticmethod(factory)
