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

import json, requests
import webbrowser
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.requester import Requester
from jenkinsapi.custom_exceptions import NoBuildData
from jenkinsapi.custom_exceptions import UnknownJob
from build_status import BuildStatus
from project_list_box_row import ProjectListBoxRow
from project_menu_item import ProjectMenuItem

class Project(object):
    
    def __init__(self, name):
        self.name = name

    def add_menu_item(self, menu):
        self.menu_item = ProjectMenuItem.factory(self.name, self.open_in_webbrowser)
        menu.append(self.menu_item)

    def add_to_listbox(self, listbox, remove_callback):
        listbox.add(ProjectListBoxRow.factory(self.name, remove_callback))

    def build_status(self):
        raise NotImplementedError()

    def open_in_webbrowser(self, widget):
        raise NotImplementedError()

class TravisProject(Project):
    travis_base_api_url = "https://api.travis-ci.org/repos/"
    travis_base_url = "https://travis-ci.org/"

    def build_status(self):
        print "status: " + self.name
        try:
            response = requests.get(TravisProject.travis_base_api_url + self.name)
            if response.status_code == requests.codes.not_found:
                status = BuildStatus.not_existing
                status.set_menu_item_icon(self.menu_item)
                return status
            json_response = json.loads(response.content)
            if not json_response:
                status = BuildStatus.not_existing
                status.set_menu_item_icon(self.menu_item)
                return status
            if json_response["last_build_result"] == 0:
                status = BuildStatus.passing
                status.set_menu_item_icon(self.menu_item)
                return status
            if json_response["last_build_result"] == None:
                status = BuildStatus.unknown
                status.set_menu_item_icon(self.menu_item)
                return status
            status = BuildStatus.failing
            status.set_menu_item_icon(self.menu_item)
        except ConnectionError:
            print "A connection error occured. Let's try again next cycle."
            status = BuildStatus.active
        return status

    def open_in_webbrowser(self, widget):
        webbrowser.open(TravisProject.travis_base_url + self.name)

class SSLRequester(Requester):
    def __init__(self, username, password, verify):
        super(SSLRequester, self).__init__(username, password)
        self.verify = verify

    def get_request_dict(self, params, headers):
        requestKWargs = super(SSLRequester, self).get_request_dict(params, headers)
        requestKWargs['verify'] = self.verify
        return requestKWargs

class JenkinsRetrieve(object):
    def __init__(self, url, username=None, password=None, verify=True):
        ssl_requester = SSLRequester(username, password, verify)
        self.jenkins = Jenkins(url, requester=ssl_requester)

    def status_of(self, name):
        raw_status_to_build_status = {"SUCCESS": BuildStatus.passing, "FAILURE": BuildStatus.failing, "UNKOWN": BuildStatus.unknown, "NOT_EXISTING": BuildStatus.not_existing}
        raw_status = self.raw_status_of(name)
        result = raw_status_to_build_status[raw_status]
        return result

    def raw_status_of(self, name):
        try:
            return self.jenkins[name].get_last_build().get_status()
        except NoBuildData:
            return 'UNKOWN'
        except UnknownJob:
            return 'NOT_EXISTING'
