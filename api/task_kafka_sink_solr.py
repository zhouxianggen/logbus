# coding: utf8
from confluent_kafka import Consumer, KafkaError


class TaskKafkaSinkSolr(Task):
    def __init__(self, bootstrap_servers, topic, solr_host, collection):
        Task.__init__(self)
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.solr_host = solr_host
        self.collection = collection

        self.consumer = Consumer({
                'bootstrap.servers': self.bootstrap_servers, 
                'group_id': self.topic})


    def do(self):
        self.consumer.subscribe([self.topic])
        while not self._exit.is_set():
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                self.log.error(msg.error())
                break
            content = msg.value().decode('utf-8')
            self.log.info(content)

