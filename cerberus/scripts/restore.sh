#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <backup.tgz|backup.tgz.enc>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="${ROOT_DIR}/deploy"
BACKUP_FILE="$1"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

if [[ "${BACKUP_FILE}" == *.enc ]]; then
  if [[ -z "${BACKUP_PASSPHRASE:-}" ]]; then
    echo "[!] BACKUP_PASSPHRASE must be set for encrypted restore"
    exit 1
  fi
  openssl enc -d -aes-256-cbc -pbkdf2 -pass env:BACKUP_PASSPHRASE -in "${BACKUP_FILE}" | tar -C "${TMP_DIR}" -xzf -
else
  tar -C "${TMP_DIR}" -xzf "${BACKUP_FILE}"
fi

pushd "${DEPLOY_DIR}" >/dev/null
docker compose cp "${TMP_DIR}/postgres.dump" postgres:/tmp/postgres.dump
docker compose exec -T postgres pg_restore -U "${DB_USER:-cerberus_app}" -d "${DB_NAME:-cerberus}" --clean --if-exists /tmp/postgres.dump

docker compose cp "${TMP_DIR}/redis.rdb" redis:/data/dump.rdb
docker compose exec -T redis redis-cli SHUTDOWN NOSAVE || true
docker compose up -d redis
popd >/dev/null

echo "[+] Restore complete"
