#!/bin/bash

source _backend.env

services=(
  unbound
  unpackerr
  watchtower
)

for service in "${services[@]}"; do
  docker compose -f "${service}.yml" --env-file ".env.${service}" up -d --force-recreate
done
