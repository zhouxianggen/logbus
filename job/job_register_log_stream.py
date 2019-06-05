# coding: utf8 
import time
from job import Job
from context import g_ctx


class JobRegisterLogStream(Job):
    def do(self):
        self.log.info('do')
        for r in g_ctx.mysql.select('log_stream', 
                ['id', 'user_id', 'app_id', 'service_id'], 
                where="WHERE status='NEW'", limit="LIMIT 10"):
            _id, user_id, app_id, service_id = r
            self.log.info('register logstream for {}.{}.{}'.format(user_id, 
                    app_id, service_id))
            name = app_id
            if service_id:
                name = '{}_{}'.format(app_id, service_id)
            
            topic = 'applog_{}'.format(name)
            r = g_ctx.kafka_admin.get_topics()
            if r.error_code:
                self.log.error('get topics failed {}:{}'.format(
                        r.error_code, r.error_desc))
                break
            if topic not in r.data:
                self.log.info('create topic {}'.format(topic))
                r = g_ctx.kafka_admin.create_topic(topic)
                if r.error_code:
                    self.log.error('create topic failed {}:{}'.format(
                            r.error_code, r.error_desc))
                    break

            r = g_ctx.kafka_connect.get_connectors()
            if r.error_code:
                self.log.error('get connectors failed {}:{}'.format(
                        r.error_code, r.error_desc))
                break
            connector = 'applog_{}_2_es'.format(name)
            if connector in r.data:
                self.log.info('delete connector {}'.format(connector))
                r = g_ctx.kafka_connect.delete_connector(connector)
                if r.error_code:
                    self.log.error('delete connector failed {}:{}'.format(
                            r.error_code, r.error_desc))
                    break
            self.log.info('create connector {}'.format(connector))
            r = g_ctx.kafka_connect.create_es_sink_connector(
                    name=connector, topics=topic, es_url=g_ctx.ES_URL)
            if r.error_code:
                self.log.error('create connector failed {}:{}'.format(
                        r.error_code, r.error_desc))
                break

            self.log.info('update logstream')
            sql = ('UPDATE log_stream SET bootstrap_servers=%s, topic=%s, '
                    'connector=%s, status=%s WHERE id=%s')
            args = (g_ctx.kafka_admin.bootstrap_servers, topic,  
                    connector, 'OK', _id)
            g_ctx.mysql.execute(sql, args)

