#!/bin/bash

docker compose -f audiobookshelf.yml --env-file .env.audiobookshelf up -d --force-recreate
docker compose -f filebrowser.yml --env-file .env.filebrowser up -d --force-recreate
docker compose -f homarr.yml --env-file .env.homarr up -d --force-recreate
docker compose -f jellyfin.yml --env-file .env.jellyfin up -d --force-recreate
docker compose -f jellyseerr.yml --env-file .env.jellyseerr up -d --force-recreate
docker compose -f profilarr.yml --env-file .env.profilarr up -d --force-recreate
docker compose -f silverbullet.yml --env-file .env.silverbullet up -d --force-recreate
docker compose -f suwayomi.yml --env-file .env.suwayomi up -d --force-recreate
docker compose -f uptime-kuma.yml --env-file .env.uptime-kuma up -d --force-recreate
docker compose -f vikunja.yml --env-file .env.vikunja up -d --force-recreate
docker compose -f watchtower.yml --env-file .env.watchtower up -d --force-recreate
