# -*- coding: utf-8 -*-
"""
    Travis-XF
    ~~~~~~~~~

    Travis-XF Travis CI extreme feedback in form of an ubuntu app-indicator.

    :copyright: (c) 2014 by Frederic Branczyk.
    :license: MIT, see LICENSE for more details.
"""

import time
from threading import Thread, Event

REFRESH_INTERVAL = 10

class TimerWithResume(object):
    def __init__(self, function):
        self.function = function
        self.abort = Event()

    def perform(self):
        while not self.abort.isSet():
            self.function()
            self.abort.wait(REFRESH_INTERVAL)

    def stop(self):
        self.abort.set()

    def start(self):
        self.thread = Thread(target=self.perform)
        self.thread.daemon = True
        self.thread.start()

    def resume(self):
        self.thread.join()
        self.abort.clear()
        self.start()
