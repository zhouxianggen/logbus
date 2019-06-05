# coding: utf8 
import json
import traceback
import configparser
import urllib.parse
from base_api import BaseApi


class ElasticsearchAdmin(BaseApi):
    def __init__(self, config):
        BaseApi.__init__(self)
        self.log.info('init by [{}]'.format(config))
        cfg = configparser.ConfigParser()
        cfg.read(config)
        self.url = cfg.get('elasticsearch', 'url').split(',')[0]


    def read_json(self, path):
        lines = []
        for ln in open(path).readlines():
            ln = ln.strip()
            if ln[:2] == '//':
                continue
            lines.append(ln)
        content = ''.join(lines)
        json.loads(content)
        return content


    def get_templates(self):
        """get templates"""
        path = '/_template'
        url = urllib.parse.urljoin(self.url, path)
        d = self.get(url, timeout=5)
        if not d:
            return self.fail('ERROR_REQUESTS_FAILED')
        return self.success(d)


    def get_template(self, name):
        """get templates"""
        path = '/_template/{}'.format(name)
        url = urllib.parse.urljoin(self.url, path)
        d = self.get(url, timeout=5)
        if not d:
            return self.fail('ERROR_REQUESTS_FAILED')
        return self.success(d)


    def create_template(self, name, fpath):
        """create template"""
        path = '/_template/{}'.format(name)
        url = urllib.parse.urljoin(self.url, path)
        data = self.read_json(fpath)
        headers = {"Content-Type": "application/json"}
        d = self.put(url, data=data, headers=headers, timeout=5)
        if not d:
            return self.fail('ERROR_REQUESTS_FAILED')
        return self.success(d)

