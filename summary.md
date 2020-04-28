### linux常用设置
1. ssh远程root登陆访问
```
vim /etc/ssh/sshd_config

#PasswordAuthentication yes  改为  PasswordAuthentication yes
PermitRootLogin prohibit-password 改为 PermitRootLogin yes
```
2. 查看系统版本 
```
cat /proc/version
lsb_release -a
```
3. pip脚本安装
```
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # 下载安装脚本
$ sudo python get-pip.py    # 运行安装脚本
```
4. 释放ip并重新分配
```
dhclient ens33 -r
dhclient ens33
```
5. python开发环境安装
```
sudo apt-get install python3 python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
```
6. 添加用户
```
groupadd -r 用户组 && useradd -r -g 用户组 用户名
```
7. ubuntu18.04修改ip
```
sudo vim /etc/netplan/50-cloud-init.yaml
network:
    ethernets:
        ens160:
            addresses:
                - 210.72.92.28/24 # IP及掩码
            gateway4: 210.72.92.254 # 网关
            nameservers:
                addresses:
                    - 8.8.8.8 # DNS
    version: 2
sudo netplan apply
```
8. 设置网卡混杂模式
```
ifconfig eth1 promisc  设置混杂模式
ifconfig eth1 -promisc 取消混杂模式
```
9. 解决linux下中文文件名显示乱码问题
```
apt-get install convmv 
convmv -f gbk -t utf-8 -r --notest /home/wwwroot 

常用参数：
-r 递归处理子文件夹
–-notest 真正进行操作，默认情况下是不对文件进行真实操作
–list 显示所有支持的编码
–unescap 可以做一下转义，比如把%20变成空格
-i 交互模式（询问每一个转换，防止误操作）
linux下有许多方便的小工具来转换编码：
    文本内容转换 iconv
    文件名转换 convmv
    mp3标签转换 python-mutagen
```
10. ubuntu 清理安装包
```
sudo apt-get autoclean      # 清理旧版本的软件缓存
sudo apt-get clean          # 清理所有软件缓存
sudo apt-get autoremove     # 删除系统不再使用的孤立软件

sudo apt-get remove --purge 软件名
sudo apt-get autoremove

# 清理旧版本的软件缓存
dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P
```

### docker常用设置
1. docker在线安装
```
wget -qO- https://get.docker.com/ | sh
wget -Y on -e "http_proxy=https://iiebc:iiecncert@192.168.1.201:3128" -qO- https://get.docker.com/ | sh
wget -qO- https://get.docker.com/ | sh
sudo groupadd docker
sudo usermod -aG docker $USER

vim /etc/docker/daemon.json
{
    "registry-mirrors": ["http://hub-mirror.c.163.com"]
}
```
2. docker离线安装
```
https://download.docker.com/linux/ubuntu/dists/

sudo dpkg -i docker-ce-cli_xxx.deb
sudo dpkg -i containerd.io_xxx.deb
sudo dpkg -i docker-ce_xxx.deb
sudo groupadd docker
sudo usermod -aG docker $USER
```
3. docker compose在线安装
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```
4. docker compose离线安装
```
sudo mv docker-compose-Linux-x86_64 /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose 
```
5. docker-compose 命令自动补全
```
yum -y install bash-completion
apt -y install bash-completion
curl -L https://raw.githubusercontent.com/docker/compose/1.25.0/contrib/completion/bash/docker-compose -o docker-compose
sudo cp docker-compose /usr/share/bash-completion/completions/
source /usr/share/bash-completion/completions/docker*
```
6. 修改镜像源
```
RUN sed -i 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//http:\/\/mirrors\.163\.com\/ubuntu\//g' /etc/apt/sources.list
sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
```
7. docker镜像报错
```
ImportError: No module named _sysconfigdata_nd
sudo ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/
```

### zabbix常用设置
1. 安装中文语言包和中文字符集
```
locale -a    # 查看已安装的语言包
sudo apt-get install language-pack-zh-hans
sudo apt-get install language-pack-zh-hant

cd /usr/share/locales    
sudo ./install-language-pack zh_CN   # 开始安装zh_CN中文字符集
sudo ./install-language-pack zh_HK   # 开始安装zh_HK中文字符集

sudo vim /etc/environment     # 配置环境变量配置文件
LC_CTYPE＝"zh_CN.UTF-8"
```

2. zabbix解决中文乱码
```
sudo vim /usr/share/zabbix/include/locales.inc.php    # 将不需要的语言设置为false
C:\Windows\Fonts 目录下拷贝字体文件到 /usr/share/zabbix/fonts
sed -i 's/graphfont/SimHei/g' /usr/share/zabbix/include/defines.inc.php    # 字体替换
```
3. zabbix自带mysql模板配置
```
# 创建mysql用户
> GRANT USAGE ON *.* TO 'monitor'@'localhost' IDENTIFIED BY 'monitor';
> FLUSH PRIVILEGES;

vim /etc/zabbix/.my.cnf
[mysql]
host     = localhost
user     = monitor
password = monitor
socket   = /run/mysqld/mysqld.sock
[mysqladmin]
host     = localhost
user     = monitor
password = monitor
socket   = /run/mysqld/mysqld.sock

cd /etc/zabbix/zabbix_agentd.d
sed -i 's@/var/lib/zabbix@/etc/zabbix@g' userparameter_mysql.conf
systemctl restart zabbix-agent
```

### mysql常用设置
1. mysql修改字符集
```
vim /etc/mysql/mysql.conf.d/mysqld.cnf
[client]
default-character-set=utf8

[mysqld]
character-set-server=utf8 
collation-server=utf8_general_ci
```

2. 修改数据库:  
```
ALTER DATABASE database_name CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;  
```
3. 修改表:  
```
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
```
4. 修改表字段:  
```
ALTER TABLE table_name CHANGE column column_name VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```


### docker部署gitlab
```
docker run -d --name gitlab --hostname gitlab --restart always -p 4443:443 -p 8080:80 -p 2222:22 -v ~/gitlab/config:/etc/gitlab -v ~/gitlab/data:/var/opt/gitlab -v ~/gitlab/logs:/var/log/gitlab gitlab/gitlab-ce
```


### portainer_agent
1. docker network create --driver overlay --attachable portainer_agent_network
2. docker service create \
    --name portainer_agent \
    --network portainer_agent_network \
    -e AGENT_CLUSTER_ADDR=tasks.portainer_agent \
    --mode global \
    --constraint 'node.platform.os == linux' \
    --mount type=bind,src=//var/run/docker.sock,dst=/var/run/docker.sock \
    --mount type=bind,src=//var/lib/docker/volumes,dst=/var/lib/docker/volumes \
    portainer/agent
3. docker service create \
    --name portainer \
    --network portainer_agent_network \
    --publish 9000:9000 \
    --publish 8000:8000 \
    --replicas=1 \
    --constraint 'node.role == manager' \
    portainer/portainer -H "tcp://tasks.portainer_agent:9001" --tlsskipverify


### 创建git 仓库
```
# 添加一个Git用户和组
adduser --system --shell /bin/bash --gecos 'git version control by pi' --group --home /home/git git
passwd git

mkdir test.git
cd test.git
git --bare init

git remote add [仓库名] [your name]@[your IP]:/home/leilei/test.git
git add .
git commit -am "Initial"
git push pi master -f
```