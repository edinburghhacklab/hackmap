#!/bin/sh
cd /app
export PYTHONUNBUFFERED=1
. /opt/pysetup/.venv/bin/activate
python ./manage.py migrate
exec python ./manage.py runserver --noreload 0.0.0.0:8000
