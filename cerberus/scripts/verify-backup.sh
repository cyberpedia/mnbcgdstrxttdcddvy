#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <backup.tgz|backup.tgz.enc>"
  exit 1
fi

BACKUP_FILE="$1"
CHECKSUM_FILE="${BACKUP_FILE}.sha256"

if [[ ! -f "${CHECKSUM_FILE}" ]]; then
  echo "[!] Missing checksum file: ${CHECKSUM_FILE}"
  exit 1
fi

sha256sum -c "${CHECKSUM_FILE}"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

if [[ "${BACKUP_FILE}" == *.enc ]]; then
  if [[ -z "${BACKUP_PASSPHRASE:-}" ]]; then
    echo "[!] BACKUP_PASSPHRASE must be set for encrypted verify"
    exit 1
  fi
  openssl enc -d -aes-256-cbc -pbkdf2 -pass env:BACKUP_PASSPHRASE -in "${BACKUP_FILE}" | tar -C "${TMP_DIR}" -xzf -
else
  tar -C "${TMP_DIR}" -xzf "${BACKUP_FILE}"
fi

for required in postgres.dump redis.rdb deploy.env; do
  [[ -f "${TMP_DIR}/${required}" ]] || { echo "[!] Missing ${required} in backup"; exit 1; }
done

echo "[+] Backup verification passed"
