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

class BuildServerBuilder(object):
    def __init__(self, box):
        self.box = box

    def add_form(self):
        raise NotImplementedError()

    def build(self):
        raise NotImplementedError()

    def remove(self):
        for row in self.rows:
            self.box.remove(row)

class JenkinsServerBuilder(BuildServerBuilder):
    def add_form(self):
        #name
        name_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.add(name_row)
        self.name_label = Gtk.Label("Name", xalign=0)
        self.name_entry = Gtk.Entry(xalign=0)
        name_row.pack_start(self.name_label, True, True, 0)
        name_row.pack_start(self.name_entry, False, True, 0)

        #host
        host_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.add(host_row)
        self.host_label = Gtk.Label("Host", xalign=0)
        self.host_entry = Gtk.Entry(xalign=0)
        host_row.pack_start(self.host_label, True, True, 0)
        host_row.pack_start(self.host_entry, False, True, 0)

        #user
        user_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.add(user_row)
        self.user_label = Gtk.Label("User", xalign=0)
        self.user_entry = Gtk.Entry(xalign=0)
        user_row.pack_start(self.user_label, True, True, 0)
        user_row.pack_start(self.user_entry, False, True, 0)

        #password
        pass_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.add(pass_row)
        self.pass_label = Gtk.Label("Password", xalign=0)
        self.pass_entry = Gtk.Entry(xalign=0)
        self.pass_entry.set_visibility(False)
        pass_row.pack_start(self.pass_label, True, True, 0)
        pass_row.pack_start(self.pass_entry, False, True, 0)

        #secure?
        secure_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.add(secure_row)
        self.secure_label = Gtk.Label("Verify SSL?", xalign=0)
        self.secure_check = Gtk.CheckButton()
        self.secure_check.set_active(True)
        secure_row.pack_start(self.secure_label, True, True, 0)
        secure_row.pack_start(self.secure_check, False, True, 0)

        self.rows = [name_row, host_row, user_row, pass_row, secure_row]

    def build(self):
        name = self.name_entry.get_text()
        host = self.host_entry.get_text()
        username = self.user_entry.get_text()
        password = self.pass_entry.get_text()
        secure = self.secure_check.get_active()
        return JenkinsBuildServer(name, host, username=username, password=password, verify=secure)

class TravisCIEnterpriseServerBuilder(BuildServerBuilder):
    def add_form(self):
        #name
        name_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.add(name_row)
        self.name_label = Gtk.Label("Name", xalign=0)
        self.name_entry = Gtk.Entry(xalign=0)
        name_row.pack_start(self.name_label, True, True, 0)
        name_row.pack_start(self.name_entry, False, True, 0)

        #host
        host_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.box.add(host_row)
        self.host_label = Gtk.Label("Host", xalign=0)
        self.host_entry = Gtk.Entry(xalign=0)
        host_row.pack_start(self.host_label, True, True, 0)
        host_row.pack_start(self.host_entry, False, True, 0)

        #token
        token_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.box.add(token_row)
        self.token_label = Gtk.Label("Token", xalign=0)
        self.token_entry = Gtk.Entry(xalign=0)
        token_row.pack_start(self.token_label, True, True, 0)
        token_row.pack_start(self.token_entry, False, True, 0)

        self.rows = [name_row, host_row, token_row]

    def build(self):
        name = self.name_entry.get_text()
        host = self.host_entry.get_text()
        token = self.token_entry.get_text()
        return TravisCIEnterprise(name, host, token)

class TravisCIComBuilder(BuildServerBuilder):
    def add_form(self):
        #token
        token_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.box.add(token_row)
        self.token_label = Gtk.Label("Token", xalign=0)
        self.token_entry = Gtk.Entry(xalign=0)
        token_row.pack_start(self.token_label, True, True, 0)
        token_row.pack_start(self.token_entry, False, True, 0)

        self.rows = [token_row]

    def build(self):
        token = self.token_entry.get_text()
        return TravisCICom(token)
