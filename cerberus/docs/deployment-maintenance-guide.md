# Deployment & Maintenance Guide

## 1. Prerequisites

- Ubuntu 22.04+ host
- Docker + Compose plugin
- UFW + fail2ban configured
- Secrets files prepared under `cerberus/deploy/secrets/`

## 2. Deploy

```bash
cp cerberus/deploy/.env.example cerberus/deploy/.env
chmod 600 cerberus/deploy/secrets/*.txt
./cerberus/scripts/deploy-stack.sh
```

## 3. Systemd Management

Install `systemd/cerberus-containers.service` to `/etc/systemd/system/` and run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cerberus-containers.service
```

## 4. Maintenance Mode

```bash
./cerberus/scripts/maintenance-mode.sh on
./cerberus/scripts/maintenance-mode.sh off
```

## 5. Backups

```bash
./cerberus/scripts/backup.sh
BACKUP_PASSPHRASE='strong-passphrase' ./cerberus/scripts/backup.sh
```

## 6. Restore

```bash
./cerberus/scripts/restore.sh <backup-file>
```

## 7. Logs Aggregation and Monitoring

Enable compose profile:

```bash
docker compose --profile observability up -d
```

This starts Loki, Promtail, Prometheus, exporters, Alertmanager, and Grafana dashboards.

## 8. Operational SOP

See `docs/operational-sop-phase9.md` for scheduled checks and incident workflows.

## 9. Upgrade Workflow

```bash
./cerberus/scripts/update-patch.sh
```

## 10. Disaster Recovery Notes

- Keep encrypted backups off-host.
- Test restore quarterly.
- Rotate compromised secrets and redeploy immediately.
