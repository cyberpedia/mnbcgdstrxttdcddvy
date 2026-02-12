# Phase 9 Operational SOP (Maintenance & Monitoring)

## 1) Log aggregation (infra, backend, frontend, notifications)

1. Start observability profile:
   ```bash
   cd cerberus/deploy
   docker compose --profile observability up -d
   ```
2. Validate Loki pipeline:
   - Promtail tails Docker logs and sends to Loki.
   - Grafana > Explore > Loki datasource > query `{job="docker"}`.
3. Notification log tracking:
   - Websocket/email/admin-alert actions are persisted in backend audit logs.
   - Query `/audit` for timeline and `/audit/support-tickets` for support flow.

## 2) Health dashboard (DB, Redis, containers, workers)

- Grafana dashboard: **Cerberus Operations Dashboard** (provisioned automatically).
- Included telemetry:
  - Backend/frontend HTTP probe status (blackbox exporter)
  - Postgres exporter metrics
  - Redis exporter metrics
  - cAdvisor container CPU/usage
  - Loki error log stream
- Run a CLI health summary:
  ```bash
  ./cerberus/scripts/health-check.sh
  ```

## 3) Backup rotation & verification

- Daily backup:
  ```bash
  BACKUP_RETENTION_DAYS=14 BACKUP_PASSPHRASE='<passphrase>' ./cerberus/scripts/backup.sh
  ```
- Verify integrity after backup:
  ```bash
  BACKUP_PASSPHRASE='<passphrase>' ./cerberus/scripts/verify-backup.sh cerberus/backups/<archive>.tgz.enc
  ```
- Rotation is automatic in `backup.sh` via `find -mtime` retention pruning.

## 4) Scheduled audit checks

- Script:
  ```bash
  ANOMALY_THRESHOLD=50 ./cerberus/scripts/scheduled-audit-check.sh
  ```
- Behavior:
  - Counts high-risk actions (`auth.login`, `notification.email`, `notification.ws`).
  - Sends admin anomaly alert email notification when threshold is exceeded.
- Recommended cadence: every 15 minutes via cron/systemd timer.

## 5) Update/patch workflow

Use the one-command patch workflow:

```bash
./cerberus/scripts/update-patch.sh
```

This executes:
1. Maintenance mode ON
2. Re-deploy/rebuild stack
3. Post-deploy health checks
4. Maintenance mode OFF

## 6) Admin alerts for anomalies

- Alertmanager routes alerts to backend webhook endpoint:
  - `POST /notifications/admin-alert`
- Result:
  - Alert is persisted to notifications
  - Audit trail entry created as `notification.admin_alert`

## 7) User support flow integration

- User submits support ticket:
  - `POST /notifications/support-ticket`
- Admin reviews support tickets:
  - `GET /audit/support-tickets`

## 8) Operations runbook checks

- Every day:
  - Dashboard red/critical panels clear.
  - New backup exists and verifies cleanly.
- Every week:
  - Execute restore dry run in staging.
  - Review audit anomaly trend.
- Every month:
  - Rotate secrets and admin credentials.
  - Patch base images and rerun `update-patch.sh`.
