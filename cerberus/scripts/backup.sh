#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="${ROOT_DIR}/deploy"
BACKUP_DIR="${ROOT_DIR}/backups"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ARCHIVE="${BACKUP_DIR}/cerberus-backup-${STAMP}.tgz"
DB_NAME="${DB_NAME:-cerberus}"
DB_USER="${DB_USER:-cerberus_app}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"

mkdir -p "${BACKUP_DIR}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

DB_PASSWORD="$(cat "${DEPLOY_DIR}/secrets/db_password.txt")"
export PGPASSWORD="${DB_PASSWORD}"

pushd "${DEPLOY_DIR}" >/dev/null
docker compose exec -T postgres pg_dump -U "${DB_USER}" -d "${DB_NAME}" -F c > "${TMP_DIR}/postgres.dump"
docker compose exec -T redis redis-cli --rdb /data/dump.rdb >/dev/null
docker compose cp redis:/data/dump.rdb "${TMP_DIR}/redis.rdb"
popd >/dev/null

cp "${DEPLOY_DIR}/.env" "${TMP_DIR}/deploy.env"

# Encrypt backup archive with OpenSSL if BACKUP_PASSPHRASE set.
if [[ -n "${BACKUP_PASSPHRASE:-}" ]]; then
  tar -C "${TMP_DIR}" -czf - . | openssl enc -aes-256-cbc -pbkdf2 -salt -pass env:BACKUP_PASSPHRASE -out "${ARCHIVE}.enc"
  sha256sum "${ARCHIVE}.enc" > "${ARCHIVE}.enc.sha256"
  echo "[+] Encrypted backup created: ${ARCHIVE}.enc"
else
  tar -C "${TMP_DIR}" -czf "${ARCHIVE}" .
  sha256sum "${ARCHIVE}" > "${ARCHIVE}.sha256"
  echo "[+] Backup created: ${ARCHIVE}"
fi

find "${BACKUP_DIR}" -type f \( -name 'cerberus-backup-*.tgz' -o -name 'cerberus-backup-*.tgz.enc' -o -name '*.sha256' \) -mtime +"${BACKUP_RETENTION_DAYS}" -delete
echo "[+] Rotation complete (retention=${BACKUP_RETENTION_DAYS} days)"
