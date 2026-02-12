# Security Best Practices

## Application Security

- Enforce RBAC at API and UI layers.
- Require CSRF for all state-changing operations.
- Sanitize user-controlled strings before render/storage.
- Keep security middleware enabled in production.

## Transport Security

- Enforce HTTPS in production.
- Use modern TLS settings and secure ciphers.
- Set HSTS, CSP, X-Frame-Options, and nosniff headers.

## Secret Management

- Never commit plaintext secrets to git.
- Use Docker secrets files with strict permissions.
- Prefer vault/KMS integration for production rotation.

## Data Integrity

- Sign critical payloads (events/leaderboard).
- Verify signatures when consumed by downstream systems.
- Hash and antivirus-scan uploaded artifacts.

## Operational Security

- Restrict ingress with firewall allowlists.
- Run containers as non-root where possible.
- Enable evidence lock mode during incident triage.
- Require confirmation phrase for destructive admin actions.

## Monitoring and Response

- Aggregate logs centrally (Loki/Promtail or equivalent).
- Alert on auth anomalies, rate-limit spikes, and destructive actions.
- Retain audit logs with immutable storage policy where possible.

## Secure CI/CD

- Run lint/security scans/tests on every PR.
- Build container images in CI to catch supply-chain drift.
- Pin dependencies and rebuild regularly for security patches.
