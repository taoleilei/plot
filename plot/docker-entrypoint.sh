#!/bin/bash

set -e

uwsgi_folder="/run/uwsgi/app/uwsgi"

project_dir="/var/www/webroot"

nginx_default="/etc/nginx/sites-enabled/default"

uwsgi_file="${project_dir}/uwsgi.ini"

nginx_file="${project_dir}/nginx.conf"

if [[ ! -d "$uwsgi_folder" ]]; then
    mkdir -p "$uwsgi_folder"
fi

if [[ -f "$uwsgi_file" ]]; then
    ln -s ${uwsgi_file} /etc/uwsgi/apps-enabled/
else
    echo "uwsgi file does not exist!"
    exit 1
fi

if [[ -f "$nginx_file" ]]; then
    #sed -i '/user/{s/www-data/root/g}' /etc/nginx/nginx.conf
    if [[ -e "$nginx_default" ]]; then
        rm ${nginx_default}
    fi
    ln -s ${nginx_file} ${nginx_default}
else
    echo "nginx file does not exist!"
    exit 1
fi

nginx
uwsgi --ini ${uwsgi_file}

exec "$@"