#!/bin/sh
cd /app
export PYTHONUNBUFFERED=1
poetry run python ./manage.py migrate
poetry run python ./socket_server.py &
exec poetry run python ./manage.py runserver --noreload 0.0.0.0:8000
