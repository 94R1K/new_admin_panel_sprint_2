#!/usr/bin/env bash

set -e

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

chown www-data:www-data /var/log

uwsgi --strict --ini /opt/app/uwsgi.ini
