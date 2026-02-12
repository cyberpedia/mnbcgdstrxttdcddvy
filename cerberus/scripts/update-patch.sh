#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[+] Enabling maintenance mode"
"${ROOT_DIR}/scripts/maintenance-mode.sh" on

echo "[+] Pulling latest images and rebuilding"
"${ROOT_DIR}/scripts/deploy-stack.sh"

echo "[+] Running post-update health checks"
"${ROOT_DIR}/scripts/health-check.sh"

echo "[+] Disabling maintenance mode"
"${ROOT_DIR}/scripts/maintenance-mode.sh" off

echo "[+] Update/patch workflow completed"
