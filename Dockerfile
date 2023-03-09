FROM python:alpine

ENV TZ=America/New_York

COPY requirements.txt /requirements.txt

RUN addgroup app \
  && adduser -S -g app app \
  && apk update \
  && apk add --no-cache bash sudo tzdata mariadb-connector-c-dev \
  && apk add --no-cache --virtual .build-deps gcc libffi-dev openssl-dev musl-dev mariadb-dev \
  && mkdir /app \
  && python3 -m venv /app/env \
  && /app/env/bin/python -m pip install -r requirements.txt \
  && chown -R app:app /app \
  && apk del .build-deps

RUN echo "01 * * * * . /app/.env && /app/env/bin/python /app/manage.py runcrons >> /tmp/cron.log 2>&1" >> /etc/crontabs/app
RUN echo "app ALL=(root) NOPASSWD: /usr/sbin/crond" >> /etc/sudoers 

COPY --chown=app:app *.py entrypoint.sh /app/
COPY --chown=app:app savings_tracker /app/savings_tracker

USER app

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["bash", "entrypoint.sh"]