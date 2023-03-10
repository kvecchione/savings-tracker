# Savings Tracker

## Overview

Savings Tracker (working title) is a Django-based web application I wrote to handle creating "virtual" savings accounts for my family. It can be used to track transactions and monthly scheduled transactions. It doesn't have many features right now but it does now what we needed it to do. I've really only exposed the ability to add a transaction/transfer to the UI at this time. All other create/delete/modify is done with the Django admin which is protected with credentials.

I certainly *could* extend it to add more features, but there are better applications out there that do similar accounting-related things better - and I'd recommend using those. I really just wrote this to have some fun with Django code.

## Running It

This can be run locally with `python manage.py runserver` or can be built into a container image and run accordingly. For the initial create there is still some manual work required to create the database and generate admin credentials for the Admin UI. 

 The latest image I have published is here: `ghcr.io/kvecchione/savings-tracker:latest`

Running this requires some environment variables to be set to connect to the database, or it defaults to running sqlite3 (not a good idea in containers with shared storage).

`DJANGO_SECRET` - Django secret key, make something up that's secure

`DJANGO_DB_ENGINE` - Defaults to sqlite3, but this can be set to mysql - I don't have support for others right now.

`MYSQL_HOSTNAME` - Database hostname

`MYSQL_PORT` - Database port, defaults to 3306

`MYSQL_DATABASE` - Database name

`MYSQL_USERNAME` - Database username

`MYSQL_PASSWORD` - Database password

The container runs a cron job every hour to trigger the check for monthly scheduled transfers.

## Look and feel

Thanks to Bootstrap, the look and feel is simple, but clean. Both desktop and mobile are functional.

### Homepage
<img src="https://github.com/kvecchione/savings-tracker/blob/main/docs/images/home.png?raw=true" width="500">

### Transfers
<img src="https://github.com/kvecchione/savings-tracker/blob/main/docs/images/transfer.png?raw=true" width="500">

### Transaction List
<img src="https://github.com/kvecchione/savings-tracker/blob/main/docs/images/transactions.png?raw=true" width="500">

### Scheduled Transfers
<img src="https://github.com/kvecchione/savings-tracker/blob/main/docs/images/scheduled.png?raw=true" width="500">

### Mobile Example
<img src="https://github.com/kvecchione/savings-tracker/blob/main/docs/images/mobile_transfer.png?raw=true" width="300">
