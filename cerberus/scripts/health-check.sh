#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="${ROOT_DIR}/deploy"

pushd "${DEPLOY_DIR}" >/dev/null

echo "== Compose Service Health =="
docker compose ps

echo "\n== Backend Health =="
docker compose exec -T backend python - <<'PY'
import requests
resp = requests.get("http://localhost:8000/health", timeout=5)
print(resp.status_code, resp.text)
PY

echo "\n== PostgreSQL Health =="
docker compose exec -T postgres pg_isready -U "${DB_USER:-cerberus_app}" -d "${DB_NAME:-cerberus}"

echo "\n== Redis Health =="
docker compose exec -T redis redis-cli ping

echo "\n== Worker/Notification Queue Check =="
docker compose exec -T backend python - <<'PY'
from app.repositories.memory_store import store
print({"notifications": len(store.notifications), "audit_logs": len(store.audit_logs)})
PY

popd >/dev/null
