# Scripts

## Deployment

- `deploy-stack.sh`: one-command production deployment for compose stack.
- `maintenance-mode.sh`: toggles frontend maintenance mode page.

## Data operations

- `backup.sh`: Postgres + Redis backup (supports OpenSSL encryption via `BACKUP_PASSPHRASE`).
- `restore.sh`: restore from backup archive.


## Testing

- `test-suite.sh`: runs Phase 8 unit/integration/security/e2e suites with coverage outputs.
Automation scripts for local development and CI/CD tasks.
