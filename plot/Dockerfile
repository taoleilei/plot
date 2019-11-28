FROM ubuntu:16.04
MAINTAINER taoleilei <taoleilei6176@163.com>


COPY sources.list /etc/apt


RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32

RUN apt-get update 

RUN apt-get -y install musl-dev libxslt-dev build-essential \ 
    libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev libmysqlclient-dev \ 
    libtiff5-dev libjpeg-dev libfreetype6-dev liblcms2-dev libwebp-dev python \ 
    python-dev python-pip uwsgi uwsgi-plugin-python nginx

COPY requirements.txt /var/www/

WORKDIR /var/www/

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

EXPOSE 80

WORKDIR /

COPY docker-entrypoint.sh ./

RUN chmod u+x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]