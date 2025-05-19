FROM python:3.11-alpine AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base AS builder
RUN apk add --no-cache --virtual .build-deps musl-dev gcc openldap-dev libffi-dev
RUN pip install poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install

FROM base AS production
RUN apk add --no-cache --virtual .build-deps musl-dev gcc openldap-dev libffi-dev
COPY --from=builder $VENV_PATH $VENV_PATH
COPY . /app

WORKDIR /app
ENTRYPOINT ["/app/contrib/entrypoint.sh"]
