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

from locale import gettext as _

import logging
logger = logging.getLogger('xf_indicator')

from xf_indicator_lib.help_dialog import HelpDialog
from build_status import BuildStatus
from ui_build_status import UiBuildStatus

# See xf_indicator_lib.HelpDialog.py for more details about how this class works.
class XfIndicatorHelpDialog(HelpDialog):
    __gtype_name__ = "HelpXfIndicatorDialog"
    _instance = None

    @classmethod
    def instance(self):
        if XfIndicatorHelpDialog._instance is None:
            XfIndicatorHelpDialog._instance = XfIndicatorHelpDialog()
        return XfIndicatorHelpDialog._instance
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the help dialog"""
        super(XfIndicatorHelpDialog, self).finish_initializing(builder)

        # only hide window, don't destroy on close button
        self.connect('delete-event', lambda w, e: w.hide() or True)

        image = builder.get_object("passing-build-status-image")
        label = builder.get_object("passing-build-status-description")
        UiBuildStatus.by_build_status(BuildStatus.passing).set_icon_name(image)
        UiBuildStatus.by_build_status(BuildStatus.passing).set_text(label)

        image = builder.get_object("unknown-build-status-image")
        label = builder.get_object("unknown-build-status-description")
        UiBuildStatus.by_build_status(BuildStatus.unknown).set_icon_name(image)
        UiBuildStatus.by_build_status(BuildStatus.unknown).set_text(label)

        image = builder.get_object("not-existing-build-status-image")
        label = builder.get_object("not-existing-build-status-description")
        UiBuildStatus.by_build_status(BuildStatus.not_existing).set_icon_name(image)
        UiBuildStatus.by_build_status(BuildStatus.not_existing).set_text(label)

        image = builder.get_object("failing-build-status-image")
        label = builder.get_object("failing-build-status-description")
        UiBuildStatus.by_build_status(BuildStatus.failing).set_icon_name(image)
        UiBuildStatus.by_build_status(BuildStatus.failing).set_text(label)
