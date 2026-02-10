# Cerberus CTF Platform - Phase 0 (Ubuntu Server Baseline)

This repository contains reproducible hardening and bootstrap assets for an Ubuntu 22.04 LTS host intended to run Cerberus.

## What this setup does

- Applies package updates and security patches.
- Configures timezone, locale, and NTP.
- Installs and hardens:
  - Docker Engine + Docker Compose plugin
  - PostgreSQL
  - Redis
  - UFW firewall
  - fail2ban for SSH brute-force protection
- Creates a least-privilege `cerberus` system user and directories under `/opt/cerberus`.
- Installs systemd units for repeatable deployment.

## Quick start (one command)

Run on a fresh Ubuntu 22.04 host as root:

```bash
curl -fsSL https://example.invalid/phase0-setup.sh | sudo bash
```

If running from a checked-out repository:

```bash
sudo CERBERUS_DB_PASSWORD='<strong-password>' ./scripts/phase0-setup.sh
```

Then place your production `docker-compose.yml` at `/opt/cerberus/docker-compose.yml` and deploy:

```bash
sudo systemctl start cerberus-deploy.service
```

## Notes

- The setup script is designed to be idempotent.
- Database credentials are read from environment variables and written with restrictive permissions.
- Redis and PostgreSQL are intended for local-only access by default.
