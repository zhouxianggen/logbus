# coding: utf8
import time
from threading import Thread, Event
from pyobject import PyObject


class Task(PyObject, Thread):
    def __init__(self):
        PyObject.__init__(self)
        Thread.__init__(self)
        self.daemon = True
        self._exit = Event()


    def run(self):
        while not self._exit.is_set():
            try:
                self.do()
            except Exception as e:
                self.log.exception(e)
                time.sleep(1)


    def do(self):
        raise NotImplementedError


    def exit(self):
        self._exit.set()

