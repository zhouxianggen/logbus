# coding: utf8
from confluent_kafka import Consumer, KafkaError


class TaskSink(PyObject):
    def __init__(self, bootstrap_servers, group_id, topic)
