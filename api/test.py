# coding: utf8 
from kafka_connect import KafkaConnect
from solr_admin import SolrAdmin
from kafka_admin import KafkaAdmin
from elasticsearch_admin import ElasticsearchAdmin


CONF = '/conf/logbus/test.conf'
KAFKA_HOSTS = 'cdh-m.isyscore.local:9092,cdh-s.isyscore.local:9092,cdh-s2.isyscore.local:9092'
ZK_HOSTS = 'cdh-m.isyscore.local:2181,cdh-s.isyscore.local:2181,cdh-s2.isyscore.local:2181'


def test_kafka_connect():
    s = KafkaConnect(CONF)
    #print(s.get_connectors())
    #print(s.get_connector('test_sensor_1_2_hbase'))
    #print(s.delete_connector('applog_test8_2_solr'))
    #print(s.create_solr_sink_connector(name="applog_test10_2_solr", topics="applog_test5", 
    #        solr_url="http://192.168.9.238:8983/solr/applog_v2/"))
    print(s.create_es_sink_connector(name="applog_yizhangarden_2_es", 
            topics="applog_yizhangarden", 
            es_url="http://10.0.0.53:9200,http://10.0.0.188:9200,http://10.0.0.36:9200"))
    #print(s.get_connectors())


def test_kafka_connect_hbase():
    s = KafkaConnectDistributed(host='http://localhost:8083')
    print(s.get_connectors())
    print(s.create_hbase_sink_connector(name="test_sensor_1_2_hbase", topics="test_sensor_1", 
            zookeeper_quorum=ZK_HOSTS))


def test_solr_admin():
    a = SolrAdmin(CONF)
    print(a.get_collections())
    #print(a.create_collection(name='test6'))


def test_kafka_admin():
    a = KafkaAdmin(CONF)
    #print(a.get_lags(topic='applog_yizhangarden', 
    #        group_id='connect-applog_yizhangarden_2_solr'))
    print(a.get_topics('applog_yizhangarden'))
    #print(a.create_topic(name='test_topic_4'))


def test_elasticsearch_admin():
    a = ElasticsearchAdmin(CONF)
    #print(a.get_templates())
    print(a.create_template(name='index_template_applog', 
            fpath='/root/work/logbus/conf/elasticsearch/index_template_applog.json'))
    #print(a.get_template('index_template_applog'))


if __name__ == '__main__':
    test_kafka_connect()
    #test_solr_admin()
    #test_kafka_admin()
    #test_elasticsearch_admin()
