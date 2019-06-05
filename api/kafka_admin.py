# coding: utf8 
import json
import traceback
import configparser
import urllib.parse
import requests
import confluent_kafka
import confluent_kafka.admin
from base_api import BaseApi


class KafkaAdmin(BaseApi):
    def __init__(self, config):
        BaseApi.__init__(self)
        self.log.info('init by {}'.format(config))
        cfg = configparser.ConfigParser()
        cfg.read(config)
        self.bootstrap_servers = cfg.get('kafka', 'bootstrap_servers')
        self.num_partitions = cfg.getint('kafka', 'num_partitions')
        self.replication_factor = cfg.getint('kafka', 'replication_factor')


    def get_lags(self, topic, group_id): #fixme
        c = confluent_kafka.Consumer({'bootstrap.servers': 
                self.bootstrap_servers, 'group.id': group_id})
        r = c.list_topics(topic)
        lags = []
        for n,t in r.topics.items():
            for pid in t.partitions.keys():
                tp = confluent_kafka.TopicPartition(n, pid, 
                        confluent_kafka.OFFSET_INVALID)
                tps = c.position([tp])
                #print(tps)
                position = tps[0].offset
                low,high = c.get_watermark_offsets(tps[0])
                lags.append({'partition': pid, 'position': position, 
                        'low': low, 'high': high, 'lag': high-position})
        return lags


    def get_topics(self, topic=None):
        producer = confluent_kafka.Producer({'bootstrap.servers': 
                self.bootstrap_servers})
        r = producer.list_topics(topic)
        topics = {}
        for k,t in r.topics.items():
            partitions = [{'id': k2, 'leader': p.leader, 
                    'replicas': p.replicas, 'isrs': p.isrs, 
                    'error': str(p.error)} for k2,p in t.partitions.items()]
            topics[k] = {'name': k, 'error': str(t.error), 
                    'partitions': partitions}
        return self.success(topics)


    def create_topic(self, name):
        """create topic"""
        topic = confluent_kafka.admin.NewTopic(name, 
                num_partitions=self.num_partitions, 
                replication_factor=self.replication_factor)
        try:
            a = confluent_kafka.admin.AdminClient({'bootstrap.servers': 
                self.bootstrap_servers})
            r = a.create_topics([topic])
            r[name].result()
            return self.success()
        except Exception as e:
            return self.fail('ERR_EXCEPTION', e)

