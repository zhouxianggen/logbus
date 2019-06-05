# coding: utf8 
import json
import configparser
import urllib.parse
from base_api import BaseApi


class KafkaConnect(BaseApi):
    def __init__(self, config):
        BaseApi.__init__(self)
        cfg = configparser.ConfigParser()
        cfg.read(config)
        self.url = cfg.get('kafka_connect', 'url')


    def get_connectors(self):
        path = '/connectors'
        url = urllib.parse.urljoin(self.url, path)
        d = self.get(url)
        if d is not None:
            return self.success(d)
        else:
            return self.fail()
    
    
    def get_connector(self, connector):
        path = '/connectors/{}'.format(connector)
        url = urllib.parse.urljoin(self.url, path)
        d = self.get(url)
        if d is not None:
            return self.success(d)
        else:
            return self.fail()

    
    def delete_connector(self, connector):
        path = '/connectors/{}'.format(connector)
        url = urllib.parse.urljoin(self.url, path)
        d = self.delete(url)
        if d is not None:
            return self.success(d)
        else:
            return self.fail()


    def create_connector(self, data):
        path = '/connectors'
        url = urllib.parse.urljoin(self.url, path)
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        d = self.post(url, data=data, headers=headers)
        if d is None:
            return self.fail('ERR_REQUEST_FAILED')
        return self.success(d)


    def create_solr_sink_connector(self, name, topics, solr_url):
        data = {
                "name": name, 
                "config" : {
                        "connector.class": "com.github.jcustenborder.kafka.connect.solr.HttpSolrSinkConnector", 
                        "topics": topics,
                        "solr.url" : solr_url,
                        "solr.queue.size" : 100,
                        "tasks.max": "1"
                        }
                }
        return self.create_connector(data)


    def create_hbase_sink_connector(self, name, topics, zookeeper_quorum): #fixme
        data = {
                "name": name, 
                "config" : {
                        "connector.class": "io.svectors.hbase.sink.HBaseSinkConnector", 
                        "topics": topics,
                        "zookeeper.quorum": zookeeper_quorum, 
                        "event.parser.class": "io.svectors.hbase.parser.JsonEventParser", 
                        "hbase.{}.rowkey.columns".format(topics): "id", 
                        "hbase.{}.rowkey.delimiter".format(topics): "|",
                        "hbase.{}.family".format(topics): "cf1",
                        "tasks.max": "1"
                        }
                }
        return self.create_connector(data)


    def create_es_sink_connector(self, name, topics, es_url):
        data = {
                "name": name, 
                "config" : {
                        "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector", 
                        "connection.url" : es_url,
                        "topics": topics,
                        "topic.index.map" : "%s:<%s_{now/d}>" % (topics, topics),
                        "key.ignore" :"true",
                        "schema.ignore": "true",
                        "type.name": "_doc",
                        "batch.size": 5000,
                        "max.buffered.records": 100000,
                        "linger.ms": 1000,
                        "connection.timeout.ms": 5000,
                        "read.timeout.ms": 5000,
                        "flush.timeout.ms": 10000,
                        "retry.backoff.ms": 1000,
                        "tasks.max": 3,
                        }
                }
        return self.create_connector(data)


