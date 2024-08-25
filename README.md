# hackmap

a django app for visualising stuff going on in the hacklab.

## development

either use nix-shell, or download:

  - pyenv / python 3.11+
  - poetry

and run `poetry env use` then `poetry run manage.py runserver` to start the django app and `poetry run python socket_server.py` in a separate terminal to start the websocket server.

formatting should be checked with `ruff`, and types with `pyright`.

## map

the map itself is an embedded svg file in `templates/map.html`. `static/js/map.js` connects to a websocket (`socket_server.py`), and then receives messages of the form:

```py
@dataclass
class WebsocketMessage:
    display: str | None
    type: str | None
    target: str | None
    state: str | None
```

if `display` is set, that HTML gets shown in the log on the right.
if `type`, `target`, and `state` are set, then all elements with `.{type}.{target}` will have their `class` replaced with `{type} {target} {state}`

`socket_server.py` just listens on some MQTT topics and broadcasts messages depending on what it sees. it also keeps track of the last `state` sent for each `type+target` combo, and resends that when a new client connects.

you need to edit the svg by hand to add things. you can use `static/map_drawing.svg` to help get the correct x/y.

## deployment

deployment is done via docker, with the following `docker-compose.yaml`:

```yaml
version: '2'
services:
  web:
    image: registry.gitlab.com/tcmal/hackmap:latest
    ports:
      - "8448:8000" # web
      - "8449:8001" # websocket
    volumes:
      - ./local_settings.py:/app/hackmap/local_settings.py # see hackmap/local_settings.py.tmpl
      - ./db.sqlite3:/app/db.sqlite3 # touch db.sqlite3
    restart: always
```

see `./scripts/deploy.sh`
