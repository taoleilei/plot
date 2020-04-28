## docker安装
- wget -qO- https://get.docker.com/ | sh

- wget -Y on -e "http_proxy=https://iiebc:iiecncert@192.168.1.201:3128" -qO- https://get.docker.com/ | sh

## 单机portainer监控
```
docker run -d -p 9000:9000 \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --name portainer-web \
    portainer/portainer
```


## 单机PXC集群创建
- 创建主节点
    ```
    docker run -d \
    -p 23306:3306 \
    -e MYSQL_ROOT_PASSWORD=iiecas \
    -e XTRABACKUP_PASSWORD=iiecas \
    -e CLUSTER_NAME=cluster1 \
    -v v1:/var/lib/mysql \
    -v backup:/data \
    -v /home/iiebc/pxc/conf:/etc/mysql/conf.d \
    -v /home/iiebc/pxc/initialdb:/docker-entrypoint-initdb.d \
    --name=node1 \
    --net=pxc-network \
    --ip=172.19.0.2 \
    pxc
    ``` 

- 创建从节点
    ```
    docker run -d \
    -p 23307:3306 \
    -e MYSQL_ROOT_PASSWORD=iiecas \
    -e XTRABACKUP_PASSWORD=iiecas \
    -e CLUSTER_NAME=cluster1 \
    -e CLUSTER_JOIN=node1 \
    -v v2:/var/lib/mysql \
    -v backup:/data \
    -v /home/iiebc/pxc/conf:/etc/mysql/conf.d \
    --name=node2 \
    --net=pxc-network \
    --ip=172.19.0.3 \
    pxc

    docker run -d \
    -p 23308:3306 \
    -e MYSQL_ROOT_PASSWORD=iiecas \
    -e XTRABACKUP_PASSWORD=iiecas \
    -e CLUSTER_NAME=cluster1 \
    -e CLUSTER_JOIN=node1 \
    -v v3:/var/lib/mysql \
    -v backup:/data \
    -v /home/iiebc/pxc/conf:/etc/mysql/conf.d \
    --name=node3 \
    --net=pxc-network \
    --ip=172.19.0.4 \
    pxc    

    docker run -d \
    -p 23309:3306 \
    -e MYSQL_ROOT_PASSWORD=iiecas \
    -e XTRABACKUP_PASSWORD=iiecas \
    -e CLUSTER_NAME=cluster1 \
    -e CLUSTER_JOIN=node1 \
    -v v4:/var/lib/mysql \
    -v backup:/data \
    -v /home/iiebc/pxc/conf:/etc/mysql/conf.d \
    --name=node4 \
    --net=pxc-network \
    --ip=172.19.0.5 \
    pxc    

    docker run -d \
    -p 23310:3306 \
    -e MYSQL_ROOT_PASSWORD=iiecas \
    -e XTRABACKUP_PASSWORD=iiecas \
    -e CLUSTER_NAME=cluster1 \
    -e CLUSTER_JOIN=node1 \
    -v v5:/var/lib/mysql \
    -v backup:/data \
    -v /home/iiebc/pxc/conf:/etc/mysql/conf.d \
    --name=node5 \
    --net=pxc-network \
    --ip=172.19.0.6 \
    pxc    
    ```

### pxc全量备份
```
docker exec -it --user root node bash
innobackupex --user=root --password=iiecas /data/backup/full
```

### pxc冷还原，需解散集群，删除容器，删除数据卷，不要删除backup卷，再新建节点
```
docker exec -it --user root node bash
cd /var/lib/mysql
mv ib_logfile0 ib_logfile1 ibdata1 ../
rm -rf /var/lib/mysql/*
mv ib_logfile0 ib_logfile1 ibdata1 /var/lib/mysql
```
1. 执行还原命令
```
innodackupex --user=root --password=iiecas --apply-back /data/backup/full/备份文件名/ # 这里的--apply-back参数指的是回滚掉全量备份之间产生的事务差异数据
```
2. 执行冷还原
```
rm -rf /var/lib/mysql/*
innobackupex --user=root --password=iiecas --copy-back /data/backup/full/备份文件名/
chown -R mysql:mysql /var/lib/mysql/
docker container restart node
```



### 目前两台haproxy的IP地址为172.19.0.7 172.19.0.8
```
docker run -it -d -p 4001:8888 -p 4002:3306 -v /home/iiebc/haproxy/h1:/usr/local/etc/haproxy --name h1 --privileged --net=pxc-network --ip=172.19.0.7 myhaproxy

docker run -it -d -p 4003:8888 -p 4004:3306 -v /home/iiebc/haproxy/h2:/usr/local/etc/haproxy --name h2 --privileged --net=pxc-network --ip=172.19.0.8 myhaproxy
```

```
haproxy -f /usr/local/etc/haproxy/haproxy.cfg
service keepalived start
```

### 样题实例部署
    ```
    docker run -d \
    -p 23306:3306 \
    -e MYSQL_ROOT_PASSWORD=iiecas \
    -e XTRABACKUP_PASSWORD=iiecas \
    -e CLUSTER_NAME=cluster2 \
    -v v1:/var/lib/mysql \
    -v backup:/data \
    -v /home/leilei/pxc/conf:/etc/mysql/conf.d \
    --name=demo1 \
    --net=demo-network \
    --ip=172.19.1.2 \
    pxc:latest

    docker run -d \
    -p 23307:3306 \
    -e MYSQL_ROOT_PASSWORD=iiecas \
    -e XTRABACKUP_PASSWORD=iiecas \
    -e CLUSTER_NAME=cluster2 \
    -e CLUSTER_JOIN=demo1 \
    -v v2:/var/lib/mysql \
    -v backup:/data \
    -v /home/leilei/pxc/conf:/etc/mysql/conf.d \
    --name=demo2 \
    --net=demo-network \
    --ip=172.19.1.3 \
    pxc:latest

    docker run -d \
    -p 8080:80 \
    -v /home/iiebc/images/j:/var/www \
    -v /usr/share/zoneinfo:/usr/share/zoneinfo \
    --name=plot \
    --net=demo-network \
    --ip=172.19.1.3 \
    plot:1.0    
    ```

### ansible命令
    ```
    ansible all -m copy -a 'src=www.tar dest=/var/www.tar'
    ansible all -m unarchive -a 'copy=false src=/var/www.tar dest=/var'

    ansible slave -m service -a 'name=uwsgi state=restarted'
    ansible slave -m service -a 'name=nginx state=restarted'

    ansible master -m service -a 'name=uwsgi state=restarted'
    ansible master -m service -a 'name=nginx state=restarted'

    ansible all -m copy -a 'src=views.py dest=/var/www/plot'
    ansible slave -m service -a 'name=uwsgi state=restarted'
    ansible slave -m service -a 'name=nginx state=restarted'
    ```


### docker部署zabbix
    ```
    docker run --name zabbix-appliance -p 80:80 -p 10051:10051 -e ZBX_SERVER_HOST="192.168.127.133" -d zabbix/zabbix-appliance:latest

    docker run --name some-zabbix-agent -e ZBX_HOSTNAME="Zabbix server" -e ZBX_SERVER_HOST="192.168.127.133" --privileged -d zabbix/zabbix-agent:latest

    docker run --name zabbix-agent -p 10050:10050 -v /proc:/data/proc -v /sys:/data/sys -v /dev:/data/dev -v /var/run/docker.sock:/var/run/docker.sock -e ZBX_SERVER_HOST="172.17.0.1" -e ZBX_HOSTNAME="taoleilei" --restart=always --privileged -d zabbix/zabbix-agent:latest

    docker service create -e ZBX_SERVER_HOST="10.255.0.1" -e ZBX_HOSTNAME="taoleilei" -p 10050:10050 zabbix/zabbix-agent:latest    
    ```
