#!/bin/bash

source _private.env

services=(
  audiobookshelf
  homarr
  jellyfin
  vikunja
)

for service in "${services[@]}"; do
  docker compose -f "${service}.yml" --env-file ".env.${service}" up -d --force-recreate
done
