## squid允许的客户端ip
- acl allcomputers src 0.0.0.0/0.0.0.0
- 配置用户名密码，后面会生成passwords文件
```
auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwords
auth_param basic realm proxy
acl authenticated proxy_auth REQUIRED
http_access allow authenticated allcomputers

sudo htpasswd -c -d /etc/squid3/passwords iiebc
tail -f /var/log/squid/access.log    
```

### 使用squid，设置apt代理  vim /etc/apt/apt.conf
```
Acquire::http::proxy "http://iiebc:iiecncert@192.168.1.201:3128/";
Acquire::https::proxy "https://iiebc:iiecncert@192.168.1.201:3128/";
Acquire::ftp::Proxy "ftp://iiebc:iiecncert@192.168.1.201:3128/";
```

### wget代理 vim /etc/wgetrc
```
http_proxy = http://iiebc:iiecncert@192.168.1.201:3128/
use_proxy = on
```

### 设置同代理环境变量
```
export http_proxy=http://iiebc:iiecncert@192.168.1.201:3128/
export http_proxy="http://iiebc:iiecncert@192.168.1.201:3128"
```

## 设置时间同步
```
server 1.cn.pool.ntp.org
server 1.asia.pool.ntp.org
server 0.asia.pool.ntp.org

sudo apt-get install ntpdate // 安装时间同步工具
sudo ntpdate cn.pool.ntp.org // 与网络服务器同步时间
date // 查看时间是否已同步
sudo hwclock --systohc //将系统时间写入硬件时间
sudo timedatectl set-timezone Asia/Shanghai

cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
```

## LVS负载均衡，解决宿主机keepalived无法正确映射问题
```
sudo apt install ipvsadm
sudo ipvsadm

ipvsadm -Ln    # 查看路由转发情况
```

## linux内核参数优化
- vim /etc/security/limits.conf 
```
*           soft   nofile       288000
*           hard   nofile       288000
*           soft   nproc        288000
*           hard   nproc        288000
*           soft  memlock      unlimited
*           hard  memlock      unlimited
root        soft   nofile       288000
root        hard   nofile       288000
root        soft   nproc        288000
root        hard   nproc        288000
root        soft  memlock      unlimited
root        hard  memlock      unlimited
``` 

- vim /etc/pam.d/common-session
```
# 追加设置
session required        pam_limits.so
```

- 登录Session全局设置 vim /etc/profile 
```
# 追加参数
ulimit -SHn 288000
vim /etc/sysctl.conf
#net.ipv4.tcp_syncookies = 1
#net.ipv4.tcp_tw_reuse = 1
#net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_fin_timeout = 30
#net.ipv4.tcp_keepalive_time = 1200 
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.tcp_max_syn_backlog = 65535
#net.ipv4.tcp_max_tw_buckets = 5000 
vm.swappiness = 0
vm.overcommit_memory = 1
fs.file-max = 288000
net.core.somaxconn = 65535
```

- 执行命令 /sbin/sysctl -p
