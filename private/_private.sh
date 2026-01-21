#!/bin/bash

source _private.env

services=(
  bazarr
  filebrowser
  jellyseerr
  lidarr
  profilarr
  radarr
  silverbullet
  sonarr
  suwayomi
  uptime-kuma
)

for service in "${services[@]}"; do
  docker compose -f "${service}.yml" --env-file ".env.${service}" up -d --force-recreate
done
