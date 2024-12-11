FROM docker.io/library/python:3.11-alpine

RUN mkdir /app
RUN apk add --no-cache --virtual .build-deps musl-dev gcc openldap-dev libffi-dev
RUN pip install poetry
COPY ./pyproject.toml /app

WORKDIR /app
RUN poetry install

COPY . /app

ENTRYPOINT ["/app/contrib/entrypoint.sh"]
