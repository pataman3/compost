#!/bin/bash

source _backend-vpn.env

services=(
  gluetun
)

for service in "${services[@]}"; do
  docker compose -f "${service}.yml" --env-file ".env.${service}" up -d --force-recreate
done
