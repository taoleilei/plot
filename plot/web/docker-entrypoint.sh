#!/bin/bash

set -e

uwsgi_folder="/run/uwsgi/app/uwsgi"

uwsgi_available="/etc/uwsgi/apps-available/uwsgi.ini"

uwsgi_enabled="/etc/uwsgi/apps-enabled/uwsgi.ini"


if [[ ! -d "$uwsgi_folder" ]]; then
    mkdir -p "$uwsgi_folder"
fi

if [[ -f "$uwsgi_available" ]]; then
    if [[ -f "$uwsgi_enabled" ]]; then
        rm ${uwsgi_enabled}
    fi
    ln -s ${uwsgi_available} ${uwsgi_enabled}
else
    echo "uwsgi file does not exist!"
    exit 1
fi

uwsgi --ini ${uwsgi_enabled}

exec "$@"