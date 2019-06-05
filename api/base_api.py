# coding: utf8 
import json
import requests
from pyobject import PyObject


class Response():

    def __init__(self, error_code='', error_desc='', data=None):
        self.error_code = error_code
        self.error_desc = error_desc
        self.data = data


    def __str__(self):
        return json.dumps({'error_code': self.error_code, 
                'error_desc': self.error_desc, 'data': self.data})


class BaseApi(PyObject):
    
    def fail(self, error_code='ERR_API_FAILED', error_desc=''):
        return Response(error_code=error_code, error_desc=error_desc)


    def success(self, data={}):
        return Response(data=data)


    def get(self, url, params=None, headers=None, timeout=5):
        try:
            r = requests.get(url, params=params, headers=headers, 
                    timeout=timeout)
            if str(r.status_code)[0] != '2':
                self.log.error('requests {} failed with {}:{}'.format(url, 
                        r.status_code, r.text))
                return None
            return json.loads(r.content)
        except Exception as e:
            self.log.exception(e)
            return None

    
    def post(self, url, data, headers=None, timeout=5):
        try:
            r = requests.post(url, data=data, headers=headers, 
                    timeout=timeout)
            if str(r.status_code)[0] != '2':
                self.log.error('requests {} failed with {}:{}'.format(url, 
                        r.status_code, r.text))
                return None
            return json.loads(r.content)
        except Exception as e:
            self.log.exception(e)
            return None


    def put(self, url, data, headers=None, timeout=5):
        try:
            r = requests.put(url, data=data, headers=headers, 
                    timeout=timeout)
            if str(r.status_code)[0] != '2':
                self.log.error('requests {} failed with {}:{}'.format(url, 
                        r.status_code, r.text))
                return None
            return json.loads(r.content)
        except Exception as e:
            self.log.exception(e)
            return None


    def delete(self, url, timeout=5):
        try:
            r = requests.delete(url, timeout=timeout)
            if str(r.status_code)[0] != '2':
                self.log.error('requests {} failed with {}:{}'.format(url, 
                        r.status_code, r.text))
                return None
            return r.status_code 
        except Exception as e:
            self.log.exception(e)
            return None

