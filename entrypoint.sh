#!/bin/bash

# Run migrations
/app/env/bin/python manage.py migrate

# Start cron
sudo -E crond -f -l 8 &

# Start webserver
/app/env/bin/python manage.py runserver 0.0.0.0:8000

exit 0