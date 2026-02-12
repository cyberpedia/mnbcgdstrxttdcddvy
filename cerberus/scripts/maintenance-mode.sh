#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 on|off"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="${ROOT_DIR}/deploy"
TARGET_PATH="/usr/share/nginx/html/maintenance.enabled"

case "$1" in
  on)
    pushd "${DEPLOY_DIR}" >/dev/null
    docker compose exec -T frontend sh -c "touch ${TARGET_PATH}"
    popd >/dev/null
    echo "[+] Maintenance mode enabled"
    ;;
  off)
    pushd "${DEPLOY_DIR}" >/dev/null
    docker compose exec -T frontend sh -c "rm -f ${TARGET_PATH}"
    popd >/dev/null
    echo "[+] Maintenance mode disabled"
    ;;
  *)
    echo "Usage: $0 on|off"
    exit 1
    ;;
esac
