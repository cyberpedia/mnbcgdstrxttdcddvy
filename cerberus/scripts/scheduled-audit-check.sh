#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="${ROOT_DIR}/deploy"
ANOMALY_THRESHOLD="${ANOMALY_THRESHOLD:-50}"

pushd "${DEPLOY_DIR}" >/dev/null
COUNT="$(docker compose exec -T backend python - <<'PY'
from app.repositories.memory_store import store
recent = [a for a in store.audit_logs if a.get('action') in {'auth.login','notification.email','notification.ws'}]
print(len(recent))
PY
)"
echo "[+] recent auditable security actions: ${COUNT}"

if (( COUNT > ANOMALY_THRESHOLD )); then
  docker compose exec -T backend python - <<'PY'
from app.api.dependencies import get_notification_service
svc = get_notification_service()
svc.send_email(0, "admin@localhost", "Cerberus anomaly alert", "Audit volume exceeded threshold.")
print("alert dispatched")
PY
fi

popd >/dev/null
