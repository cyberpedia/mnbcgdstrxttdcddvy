#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="${ROOT_DIR}/deploy"
COMPOSE_FILE="${DEPLOY_DIR}/docker-compose.yml"
ENV_FILE="${DEPLOY_DIR}/.env"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "[!] Missing ${ENV_FILE}. Copy .env.example and fill values."
  exit 1
fi

for secret in db_password.txt jwt_secret.txt signing_secret.txt; do
  if [[ ! -f "${DEPLOY_DIR}/secrets/${secret}" ]]; then
    echo "[!] Missing secret file: ${DEPLOY_DIR}/secrets/${secret}"
    exit 1
  fi
done

cd "${DEPLOY_DIR}"
docker compose --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}" pull || true
docker compose --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}" up -d --build

echo "[+] Cerberus stack deployed"
