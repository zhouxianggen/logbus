logbus - 日志管理分析平台
![](https://img.shields.io/badge/python%20-%203.7-brightgreen.svg)
========
> logbus 根据业务类型（服务、前端、后端等）提供日志接入规范，将日志数据集成到hbase和solr，并提供日志搜索分析工具。

## `文档`
+ [logstash接入日志平台规范](http://192.168.0.101/bigdatagroup/logbus/blob/master/doc/logstash_to_logbus_spec.docx)
+ [confluent connect介绍](http://192.168.0.101/bigdatagroup/logbus/blob/master/doc/intro_confluent_connect.docx)

## `API`

## `配置`
#### 接入配置
> logstash 

#### kafka 配置

#### confluent connect 配置

#### solr 配置

## `演示`
+ [logstash->kafka->connect->solr->hue](http://192.168.9.241:8888/hue/dashboard/new_search?engine=solr)
+ [kafka监控](http://192.168.9.234:8048/ke/)
+ [connectors](http://192.168.9.234:8083/connectors)
+ [solr](http://192.168.9.238:8983/solr/#/applog_test4/query)

