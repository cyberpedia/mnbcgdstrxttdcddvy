# Cerberus Monorepo (Phase 1 Placeholder)

This directory contains the initial modular structure for the Cerberus CTF platform.

## Layout

- `backend/`: Python backend services and APIs.
- `frontend/`: React frontend application.
- `docs/`: Architecture, runbooks, and security documentation.
- `scripts/`: Local automation and CI helper scripts.

## Quality and Security Baseline

- **Python**: PEP8 style with `ruff`, static typing support, and `bandit` security linting.
- **Frontend**: ESLint configuration for React + security-focused rules.

## Next Steps

- Implement backend API framework and data models.
- Implement frontend app routes and core UI.
- Wire CI for linting, tests, and security checks.


## Phase 6 Deployment

See `docs/deployment-phase6.md` for production Docker Compose deployment, systemd container orchestration, maintenance mode, backup/restore, and CI container build checks.
