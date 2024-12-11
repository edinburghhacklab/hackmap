#!/usr/bin/env sh
set -ex
docker build -t ghcr.io/edinburghhacklab/hackmap:latest .
docker push ghcr.io/edinburghhacklab/hackmap:latest
ssh -t carbon.hacklab 'sudo docker-compose -f /srv/docker/hackmap/docker-compose.yml pull && sudo docker-compose -f /srv/docker/hackmap/docker-compose.yml up --force-recreate -d'
