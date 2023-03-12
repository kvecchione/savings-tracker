FROM python:alpine

ENV TZ=UTC
COPY requirements.txt /requirements.txt

RUN addgroup app \
  && adduser -S -g app app \
  && apk update \
  && apk add --no-cache bash tzdata mariadb-connector-c-dev dcron libcap \
  && apk add --no-cache --virtual .build-deps gcc libffi-dev openssl-dev musl-dev mariadb-dev \
  && mkdir /app \
  && python3 -m venv /app/env \
  && /app/env/bin/python -m pip install -r requirements.txt \
  && chown -R app:app /app \
  && apk del .build-deps \
  && chown app:app /usr/sbin/crond \
  && setcap cap_setgid=ep /usr/sbin/crond

RUN echo "05 * * * * /app/env/bin/python /app/manage.py runcrons >> /tmp/cron.log 2>&1" > /etc/crontabs/app \
  && chown app:app /etc/crontabs/app \
  && rm /etc/crontabs/root

COPY --chown=app:app *.py entrypoint.sh /app/
COPY --chown=app:app savings_tracker /app/savings_tracker

USER app
WORKDIR /app
EXPOSE 8000

ENTRYPOINT ["bash", "entrypoint.sh"]