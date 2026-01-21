#!/bin/bash

source _private-vpn.env

services=(
  prowlarr
  qbittorrent
  sabnzbd
)

for service in "${services[@]}"; do
  docker compose -f "${service}.yml" --env-file ".env.${service}" up -d --force-recreate
done
