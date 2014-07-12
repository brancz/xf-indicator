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

from build_server import JenkinsBuildServer, TravisCIEnterprise, TravisCICom 
from gi.repository import Gtk

class BuildServerBuildStrategy(object):
    def add_form(self, row):
        raise NotImplementedError()

    def build(self, name):
        raise NotImplementedError()

class JenkinsServerBuildStrategy(BuildServerBuildStrategy):
    def add_form(self, row):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        row.add(vbox)

        #host
        host_row = Gtk.ListBoxRow()
        vbox.add(host_row)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        host_row.add(hbox)
        self.host_label = Gtk.Label("Host", xalign=0)
        self.host_entry = Gtk.Entry(xalign=0)
        hbox.pack_start(self.host_label, True, True, 0)
        hbox.pack_start(self.host_entry, False, True, 0)

        #user
        user_row = Gtk.ListBoxRow()
        vbox.add(user_row)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        user_row.add(hbox)
        self.user_label = Gtk.Label("User", xalign=0)
        self.user_entry = Gtk.Entry(xalign=0)
        hbox.pack_start(self.user_label, True, True, 0)
        hbox.pack_start(self.user_entry, False, True, 0)

        #password
        pass_row = Gtk.ListBoxRow()
        vbox.add(pass_row)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        pass_row.add(hbox)
        self.pass_label = Gtk.Label("Password", xalign=0)
        self.pass_entry = Gtk.Entry(xalign=0)
        hbox.pack_start(self.pass_label, True, True, 0)
        hbox.pack_start(self.pass_entry, False, True, 0)

        #secure?
        secure_row = Gtk.ListBoxRow()
        vbox.add(secure_row)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        secure_row.add(hbox)
        self.secure_label = Gtk.Label("Secure", xalign=0)
        self.secure_check = Gtk.CheckButton()
        self.secure_check.set_active(True)
        hbox.pack_start(self.secure_label, True, True, 0)
        hbox.pack_start(self.secure_check, False, True, 0)

    def build(self, name):
        return JenkinsBuildServer("https://ci.pondati.net/", username="flower-pot", password="Asdfmnsek123!", verify=False)

class TravisCIEnterpriseServerBuildStrategy(BuildServerBuildStrategy):
    def add_form(self, row):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.host_label = Gtk.Label("Host", xalign=0)
        self.host_entry = Gtk.Entry(xalign=0)
        hbox.pack_start(self.host_label, True, True, 0)
        hbox.pack_start(self.host_entry, False, True, 0)

    def build(self, name):
        return JenkinsBuildServer("https://ci.pondati.net/", username="flower-pot", password="Asdfmnsek123!", verify=False)
