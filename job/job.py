# coding: utf8
import time
from threading import Thread, Event
from pyobject import PyObject


class Job(PyObject, Thread):
    def __init__(self, interval=60):
        PyObject.__init__(self)
        Thread.__init__(self)
        self.daemon = True
        self.interval = interval
        self._exit = Event()


    def run(self):
        while not self._exit.is_set():
            try:
                self.do()
            except Exception as e:
                self.log.exception(e)
            time.sleep(self.interval)


    def do(self):
        pass


    def exit(self):
        self._exit.set()
