# Scripts

## Deployment

- `deploy-stack.sh`: one-command production deployment for compose stack.
- `maintenance-mode.sh`: toggles frontend maintenance mode page.

## Data operations

- `backup.sh`: Postgres + Redis backup (supports OpenSSL encryption via `BACKUP_PASSPHRASE`).
- `restore.sh`: restore from backup archive.


- `verify-backup.sh`: verifies backup checksums and archive contents.
- `health-check.sh`: checks service, DB, Redis, and queue health.
- `scheduled-audit-check.sh`: anomaly detector over audit events with admin alert escalation.
- `update-patch.sh`: maintenance-safe patch/update orchestration.

## Testing

- `test-suite.sh`: runs Phase 8 unit/integration/security/e2e suites with coverage outputs.
