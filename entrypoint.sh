#!/bin/bash

# export env vars to file for cron
env | grep MYSQL_ | sed "s/^/export /g" > /app/.env

# start cron
sudo crond -b 

# Start django
/app/env/bin/python manage.py migrate
/app/env/bin/python manage.py runserver 0.0.0.0:8000

exit 0