#!/bin/bash

services=(
  audiobookshelf
  filebrowser
  homarr
  jellyfin
  jellyseerr
  profilarr
  silverbullet
  suwayomi
  uptime-kuma
  vikunja
  watchtower
)

for service in "${services[@]}"; do
  docker compose -f "${service}.yml" --env-file ".env.${service}" up -d --force-recreate
done
