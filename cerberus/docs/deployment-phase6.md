# Phase 6 Deployment & DevOps

## Stack

- Backend: FastAPI container (`cerberus/backend/Dockerfile`)
- Frontend: React static build served by nginx (`cerberus/frontend/Dockerfile`)
- PostgreSQL + Redis services in `deploy/docker-compose.yml`
- Optional log aggregation profile with Loki + Promtail

## One-command deployment

```bash
cp cerberus/deploy/.env.example cerberus/deploy/.env
printf 'change-me\n' > cerberus/deploy/secrets/db_password.txt
printf 'change-me\n' > cerberus/deploy/secrets/jwt_secret.txt
printf 'change-me\n' > cerberus/deploy/secrets/signing_secret.txt
./cerberus/scripts/deploy-stack.sh
```

## Backup & restore

- Backup: `./cerberus/scripts/backup.sh`
- Encrypted backup: `BACKUP_PASSPHRASE='...' ./cerberus/scripts/backup.sh`
- Restore: `./cerberus/scripts/restore.sh <backup-file>`

## Maintenance mode

- Enable: `./cerberus/scripts/maintenance-mode.sh on`
- Disable: `./cerberus/scripts/maintenance-mode.sh off`

Maintenance mode creates `maintenance.enabled` in frontend web root; nginx serves `maintenance.html` with HTTP 503.

## Systemd

Use `systemd/cerberus-containers.service` on hosts where repo is installed at `/opt/cerberus`.

## Security notes

- Use Docker secrets files with `chmod 600`.
- Keep `internal` compose network isolated from host exposure.
- Enable host firewall (`ufw`) and allow only 22/80/443.
- Store backup encryption passphrase in secret manager.
- Integrate antivirus scanner in `app/core/file_security.py` for production.

## Cloud readiness layer

Compose env supports optional object-storage settings:

- `CLOUD_STORAGE_ENDPOINT`
- `CLOUD_STORAGE_BUCKET`
- `CLOUD_REGION`

These keep storage/network configuration abstracted from application code paths.
