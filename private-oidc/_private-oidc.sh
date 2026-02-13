#!/bin/bash

source _private-oidc.env

services=(
  audiobookshelf
  homarr
  jellyfin
  memos
  vikunja
)

for service in "${services[@]}"; do
  docker compose -f "${service}.yml" --env-file ".env.${service}" up -d --force-recreate
done
