#!/usr/bin/env sh
set -ex
docker build -t registry.gitlab.com/tcmal/hackmap:latest .
docker push registry.gitlab.com/tcmal/hackmap:latest
ssh -t carbon.hacklab 'sudo docker-compose -f /srv/docker/hackmap/docker-compose.yml pull && sudo docker-compose -f /srv/docker/hackmap/docker-compose.yml up --force-recreate -d'
