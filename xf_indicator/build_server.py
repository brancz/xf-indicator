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

import logging
logger = logging.getLogger('xf_indicator')

import json, requests
from urlparse import urljoin
import jenkinsapi.jenkins
from jenkinsapi.utils.requester import Requester
from jenkinsapi.custom_exceptions import NoBuildData, UnknownJob
from build_status import BuildStatus

class BuildServerList(object):
    def __init__(self, shelf=None):
        self.build_servers = []
        if shelf is not None and shelf.has_key("build_servers"):
            self.build_servers = shelf["build_servers"]
        if len(self.build_servers) is 0:
            self.build_servers.append(TravisCIOrg())

    def get(self, index):
        return self.build_servers[index]

    def add(self, build_server):
        self.build_servers.append(build_server)

    def remove(self, build_server):
        self.build_servers.remove(build_server)

    def save(self, shelf):
        shelf["build_servers"] = self.build_servers

    def __iter__(self):
        return self.build_servers.__iter__()

class TravisCIServer(object):
    def __init__(self, name, base_url, base_api_url, token):
        self.name = name
        self.base_url = base_url
        self.base_api_url = base_api_url
        self.token = token

    def latest_status_of(self, name):
        try:
            headers = {"User-Agent": "xf-indicator/0.1",
                       "Authorization": "token "+self.token}

            response = requests.get(self.base_api_url + name, headers=headers)
            if response.status_code == requests.codes.not_found:
                return BuildStatus.not_existing
            json_response = json.loads(response.content)
            if not json_response:
                return BuildStatus.not_existing
            if json_response["last_build_result"] == 0:
                return BuildStatus.passing
            if json_response["last_build_result"] == None:
                return BuildStatus.unknown
            return BuildStatus.failing
        except requests.ConnectionError:
            logger.warning("A connection error occured. Let's try again next cycle.")
            return BuildStatus.active

    def latest_build_url_of(self, name):
        return urljoin(self.base_url,  name)

    def deletable(self):
        return True

    def __str__(self):
        return self.name

class TravisCIEnterprise(TravisCIServer):
    def __init__(self, name, base_url, token):
        super(TravisCIEnterprise, self).__init__("Travis CI", base_url, urljoin(base_url, "/api"), token)

    def type(self):
        return "Travis CI Enterprise"

class TravisCIOrg(TravisCIServer):
    def __init__(self):
        super(TravisCIOrg, self).__init__("Travis CI", "https://travis-ci.org/", "https://api.travis-ci.org/", "")

    def type(self):
        return "Travis CI"

    def deletable(self):
        return False

class TravisCICom(TravisCIServer):
    def __init__(self, token):
        super(TravisCICom, self).__init__("Travis CI Pro", "https://travis-ci.com/", "https://api.travis-ci.com/", token)

    def type(self):
        return "Travis CI Pro"

class SSLRequester(Requester):
    def __init__(self, username, password, verify):
        super(SSLRequester, self).__init__(username, password)
        self.verify = verify

    def get_request_dict(self, params, headers):
        requestKWargs = super(SSLRequester, self).get_request_dict(params, headers)
        requestKWargs['verify'] = self.verify
        return requestKWargs

class JenkinsBuildServer(object):
    def __init__(self, name, url, username=None, password=None, verify=True):
        self.name = name
        self.url = url
        ssl_requester = SSLRequester(username, password, verify)
        self.jenkins = jenkinsapi.jenkins.Jenkins(url, requester=ssl_requester)

    def latest_status_of(self, name):
        raw_status_to_build_status = {"SUCCESS": BuildStatus.passing, "FAILURE": BuildStatus.failing, "UNKOWN": BuildStatus.unknown, "NOT_EXISTING": BuildStatus.not_existing}
        raw_status = self.latest_raw_status_of(name)
        result = raw_status_to_build_status[raw_status]
        return result

    def latest_raw_status_of(self, name):
        try:
            return self.jenkins[name].get_last_build().get_status()
        except NoBuildData:
            return 'UNKOWN'
        except UnknownJob:
            return 'NOT_EXISTING'

    def latest_build_url_of(self, name):
        return urljoin(self.url, "/job/" + name + "/lastBuild/")

    def deletable(self):
        return True

    def __str__(self):
        return self.name

    def type(self):
        return "Jenkins"
