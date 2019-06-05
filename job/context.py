# coding: utf8 
import configparser
from pyobject import PyObject
from pymysql import PyMySql
import sys
sys.path.insert(0, '/root/work/logbus/api')
from kafka_admin import KafkaAdmin
from kafka_connect import KafkaConnect


class Context(PyObject):
    def __init__(self):
        PyObject.__init__(self)


    def init(self, config):
        cfg = configparser.ConfigParser()
        cfg.read(config)

        self.RDS_HOST = cfg.get('rds', 'host')
        self.RDS_PORT = cfg.getint('rds', 'port')
        self.RDS_USER = cfg.get('rds', 'user')
        self.RDS_PSWD = cfg.get('rds', 'pswd')
        self.RDS_DB = cfg.get('rds', 'db')
        self.mysql = PyMySql(host=self.RDS_HOST, port=self.RDS_PORT,
                user=self.RDS_USER, pswd=self.RDS_PSWD, db=self.RDS_DB)

        self.SOLR_URL = cfg.get('solr', 'url')
        self.ES_URL = cfg.get('elasticsearch', 'url')
        
        self.kafka_admin = KafkaAdmin(config)
        self.kafka_connect = KafkaConnect(config)


g_ctx = Context()

