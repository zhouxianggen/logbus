# coding: utf8 
import json
import requests
from pyobject import PyObject


class ConfluentRESTProxy(PyObject):
    def __init__(self, restful_url):
        PyObject.__init__(self)
        self.restful_url = restful_url
        self.default_headers = {'Accept': 'application/vnd.kafka.v2+json'}


    def get(self, url, headers=None):
        if not headers:
            headers = self.default_headers
        try:
            r = requests.get(url, headers=headers, timeout=2)
            return json.loads(r.content)
        except Exception as e:
            self.log.exception(e)
            return None

    
    def post(self, url, data, headers=None):
        if not headers:
            headers = self.default_headers
        try:
            r = requests.post(url, data=data, headers=headers, timeout=2)
            return json.loads(r.content)
        except Exception as e:
            self.log.exception(e)
            return None


    def get_topics(self):
        url = '{}/topics'.format(self.restful_url)
        return self.get(url)
    
    
    def get_topic(self, topic_name):
        url = '{}/topics/{}'.format(self.restful_url, topic_name)
        return self.get(url)

    
    def get_partitions(self, topic_name):
        url = '{}/topics/{}/partitions'.format(self.restful_url, topic_name)
        return self.get(url)


    def post_message(self, topic_name, records, key_schema=None, 
            key_schema_id=None, value_schema=None, value_schema_id=None):
        url = '{}/topics/{}'.format(self.restful_url, topic_name)
        data = {'records': records}
        if key_schema:
            data['key_schema'] = key_schema
        if key_schema_id:
            data['key_schema_id'] = key_schema_id
        if value_schema:
            data['value_schema'] = value_schema
        if value_schema_id:
            data['value_schema_id'] = value_schema_id
        return self.post(url, data)


