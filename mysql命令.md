### mysql常用查看命令
命令 | 说明
-|-
show status like '%max_connections%'; | mysql最大连接数
set global max_connections=1000; | 重新设置
show variables like '%max_connections%'; | 查询数据库当前设置的最大连接数
show global status like 'Max_used_connections'; | 服务器响应的最大连接数

### mysql查看进程命令
- show status like 'Threads%'; 

Variable_name | Value |  说明  
-|-|-
Threads_cached | 0 | mysql管理的线程池中还有多少可以被复用的资源 |
Threads_connected | 152 | 打开的连接数 |
Threads_created | 550 | 表示创建过的线程数，如果发现Threads_created值过大的话，表明MySQL服务器一直在创建线程，这也是比较耗资源，可以适当增加配置文件中thread_cache_size值，查询服务器 |
Threads_running | 1 | 激活的连接数，这个数值一般远低于connected数值，准确的来说，Threads_running是代表当前并发数

```
show variables like 'thread_cache_size';
set global thread_cache_size=60;
```

### 解除正在死锁的状态有两种方法：
- 第一种：
    1. 查询是否锁表
    show OPEN TABLES where In_use > 0;
    2. 查询进程（如果您有SUPER权限，您可以看到所有线程。否则，您只能看到您自己的线程）
    show processlist
    2. 杀死进程id（就是上面命令的id列）
    kill id

- 第二种：
    1. 查看下在锁的事务
    SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX;
    2. 杀死进程id（就是上面命令的trx_mysql_thread_id列）
    kill 线程ID
        ```
        SHOW PROCESSLIST;
        KILL 420821;
        ```      

#### 其它关于查看死锁的命令：
命令 | 说明
-|-
SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX; | 查看当前的事务 
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS; | 查看当前锁定的事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS; | 查看当前等锁的事务

### 创建数据库
```
CREATE DATABASE IF NOT EXISTS x CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';
```

### 修改数据库时区
```
set global time_zone = '+8:00';
set time_zone = '+8:00';
flush privileges;
select now();
```

### 测试PXC数据库并发性能
```
mysqlslap -h192.168.1.210 -uroot -piiecas -P3306 --concurrency=1000 --iterations=2 --auto-generate-sql --auto-generate-sql-load-type=mixed --auto-generate-sql-add-autoincrement --engine=innodb --number-of-queries=10000 --debug-info
```

### 开启数据库远程连接
```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'iiecas' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```