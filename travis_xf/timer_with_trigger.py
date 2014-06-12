# -*- coding: utf-8 -*-
"""
    Travis-XF
    ~~~~~~~~~

    Travis-XF Travis CI extreme feedback in form of an ubuntu app-indicator.

    :copyright: (c) 2014 by Frederic Branczyk.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading

REFRESH_INTERVAL = 3

class TimerWithTrigger(object):
    def __init__(self, function):
        self.function = function

    def perform(self):
        while True:
            self.function()
            time.sleep(3)

    def start(self):
        self.thread = threading.Thread(target=self.perform)
        self.thread.daemon = True
        self.thread.start()
