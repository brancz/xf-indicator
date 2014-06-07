# -*- coding: utf-8 -*-
"""
    Travis-XF
    ~~~~~~~~~

    Travis-XF Travis CI extreme feedback in form of an ubuntu app-indicator.

    :copyright: (c) 2014 by Frederic Branczyk.
    :license: MIT, see LICENSE for more details.
"""

from indicator import Indicator
from gi.repository import Gtk

def main():
    travis_xf_indicator = Indicator()
    Gtk.main()
