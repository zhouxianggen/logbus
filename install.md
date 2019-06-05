
### 安装JDK
1. 下载
```
download jdk from https://www.oracle.com/technetwork/java/javase/downloads/index.html
mkdir /usr/lib/jdk
tar -zxf jdk.tar.gz -C /usr/lib/jdk
```
2. 配置系统环境
> vi /etc/profile.d/jdk.sh
```
export JAVA_HOME=/usr/lib/jdk/jdk-11.0.2
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
```
> source /etc/profile

### 安装 elasticsearch 集群

1. 在集群每台机器上，配置hosts
> vi /etc/hosts
```
10.0.0.53   es_node1
10.0.0.188  es_node2
10.0.0.36   es_node3
```

2. 下载
```
su elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.1.0-linux-x86_64.tar.gz
tar -zxf elasticsearch-7.1.0-linux-x86_64.tar.gz
mv elasticsearch-7.1.0 elasticsearch
cd elasticsearch
```

2. elasticsearch 配置
> vi config/elasticsearch.yml
```
cluster.name: logbus
node.name: es_node1 # 每台机器设置对应值
path.data: /data/data/elasticsearch
path.logs: /data/log/elasticsearch
bootstrap.memory_lock: true
network.host: 10.0.0.53 # 每台机器设置对应值
http.port: 9200
discovery.seed_hosts: ["es_node1", "es_node2", "es_node3"]
cluster.initial_master_nodes: ["es_node1", "es_node2", "es_node3"]
```

> vi config/jvm.options
```
-Xms4g
-Xmx4g
```

> vi /etc/profile.d/es.sh
```
export ES_TMPDIR=/data/tmp
export ES_HOME=/opt/elasticsearch
export PATH=$ES_HOME/bin:$PATH
export LD_LIBRARY_PATH=$ES_HOME/lib:$LD_LIBRARY_PATH
```

3. 配置系统设置
> vi /etc/security/limits.conf
```
es   -  nofile     65536
es   -  nproc      65536
es   -  memlock    unlimited
es   -  fileszie   unlimited
es   -  as         unlimited
```

> vi /etc/sysctl.conf
```
vm.max_map_count=1000000
```

> sysctl -p


4. 安装中文分词
> elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.1.0/elasticsearch-analysis-ik-7.1.0.zip

5. 运行
> elasticsearch -d -p pid

### Kibana 部署
1. 下载源码安装
```
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.1.0-linux-x86_64.tar.gz
tar -zxf kibana-7.1.0-linux-x86_64.tar.gz
mv kibana-7.1.0 kibana
cd kibana
```

2. kibana 配置
> vi config/kibana.yml
```
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://10.0.0.53:9200", "http://10.0.0.188:9200", "http://10.0.0.36:9200"]
i18n.locale: "zh-CN"
``` 

3. 运行
> ./bin/kibana

或者后台运行

> nohup /opt/kibana/bin/kibana -c /opt/kibana/config/kibana.yml &

