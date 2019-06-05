# coding: utf8 
import json
import traceback
import configparser
import urllib.parse
from base_api import BaseApi


class SolrAdmin(BaseApi):
    def __init__(self, config):
        BaseApi.__init__(self)
        self.log.info('init by [{}]'.format(config))
        cfg = configparser.ConfigParser()
        cfg.read(config)
        self.url = cfg.get('solr', 'url')
        self.configName = cfg.get('solr', 'configName')
        self.numShards = cfg.getint('solr', 'numShards')
        self.maxShardsPerNode = cfg.getint('solr', 'maxShardsPerNode')
        self.replicationFactor = cfg.getint('solr', 'replicationFactor')
        self.autoAddReplicas = cfg.getboolean('solr', 'autoAddReplicas')


    def get_collections(self):
        """get collections"""
        path = '/solr/admin/collections'
        url = urllib.parse.urljoin(self.url, path)
        params = {
                'action': 'CLUSTERSTATUS', 
                'wt': 'json'
                }

        d = self.get(url, params=params, timeout=10)
        if not d:
            return self.fail('ERROR_REQUESTS_FAILED')
        
        if d['responseHeader']['status'] == 0:
            return self.success(d['cluster']['collections'])
        else:
            return self.fail('ERR_CREATE_COLLECTION_FAILED', r.text)


    def create_collection(self, name):
        """create collection"""
        path = '/solr/admin/collections'
        url = urllib.parse.urljoin(self.url, path)
        params = {
                'name': name, 
                'action': 'CREATE', 
                'numShards': self.numShards, 
                'autoAddReplicas': self.autoAddReplicas, 
                'collection.configName': self.configName, 
                'maxShardsPerNode': self.maxShardsPerNode, 
                'replicationFactor': self.replicationFactor, 
                'router.name': 'compositeId', 
                'wt': 'json'
                }

        d = self.get(url, params=params, timeout=10)
        if not d:
            return self.fail('ERROR_REQUESTS_FAILED')
        
        if d['responseHeader']['status'] == 0:
            return self.success(d)
        else:
            return self.fail('ERR_CREATE_COLLECTION_FAILED', r.text)

