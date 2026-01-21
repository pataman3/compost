#!/bin/bash

source _public.env

services=(
  authelia
  pihole
  traefik
)

for service in "${services[@]}"; do
  docker compose -f "${service}.yml" --env-file ".env.${service}" up -d --force-recreate
done
