#!/bin/bash

BUCKET="$1"  # e.g. backend, private, public, etc.
[ -n "$BUCKET" ] || exit 1

SERVICES_DIR="services/$BUCKET"
SECRETS_DIR="secrets/$BUCKET"
BUCKET_ENV="$SECRETS_DIR/bucket.env"

[ -f "$BUCKET_ENV" ] && set -a && . "$BUCKET_ENV" && set +a

for yml_file in "$SERVICES_DIR"/*.yml; do
  [ -e "$yml_file" ] || continue

  service="$(basename "$yml_file" .yml)"
  env_file="$SECRETS_DIR/.env.$service"

  [ -f "$env_file" ] || continue

  docker compose -f "$yml_file" --env-file "$env_file" up -d --force-recreate
done
