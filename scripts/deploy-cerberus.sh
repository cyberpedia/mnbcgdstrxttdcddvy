#!/usr/bin/env bash
set -euo pipefail

CERBERUS_HOME="/opt/cerberus"
COMPOSE_FILE="${CERBERUS_HOME}/docker-compose.yml"
ENV_FILE="${CERBERUS_HOME}/.env"

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "[!] Missing ${COMPOSE_FILE}. Place your Cerberus compose file first." >&2
  exit 1
fi

cd "${CERBERUS_HOME}"

if command -v docker >/dev/null 2>&1; then
  docker compose --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}" pull
  docker compose --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}" up -d --remove-orphans
else
  echo "[!] docker not found" >&2
  exit 1
fi
