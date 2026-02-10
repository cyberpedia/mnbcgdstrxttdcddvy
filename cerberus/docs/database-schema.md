# Cerberus Database Schema (Phase 2)

This schema is designed for PostgreSQL with multi-tenant/event separation.

## Key design decisions

- `tenant_id` is included across domain entities for tenant isolation.
- `event_id` is included where event scoping is required.
- `leaderboard` supports either per-user or per-team rows using a check constraint.
- `audit_logs` stores JSON snapshots (`before`/`after`) for audit readiness.
- Password storage uses `hashed_password` only (never plaintext).
- Baseline least-privilege grants are included for application role `cerberus_app_rw`.

## Files

- SQL DDL + indexes + grants: `backend/migrations/001_phase2_schema.sql`
- SQLAlchemy models: `backend/app/models/schema.py`
