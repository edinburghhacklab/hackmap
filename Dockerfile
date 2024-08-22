FROM docker.io/library/python:3.11-alpine

RUN mkdir /app
RUN pip install poetry
COPY ./pyproject.toml /app

WORKDIR /app
RUN poetry install

COPY . /app

ENTRYPOINT ["/app/contrib/entrypoint.sh"]
