# coding: utf8 
import asyncio
import concurrent
import configparser
from pyobject import PyObject
import sys #fixme
sys.path.insert(0, '../model')
from logbus_model import LogbusModel


class Context(PyObject):
    def __init__(self):
        PyObject.__init__(self)
        self.loop = asyncio.get_event_loop()
        self.pool = concurrent.futures.ThreadPoolExecutor(
                thread_name_prefix='worker')
        self.initialized = False


    def init(self, config):
        self.log.info('init context by [{}]'.format(config))
        cfg = configparser.ConfigParser()
        cfg.read(config)
        self.model = LogbusModel(config)
        self.initialized = True


g_ctx = Context()

