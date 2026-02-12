# Cerberus Admin Guide

> Version: Phase 7

## 1. Role Model

Cerberus supports layered RBAC roles:
- Super Admin
- Admin
- Event Admin
- Challenge Author
- Infra Admin
- User

Admins should grant the lowest role necessary for each operator.

## 2. Event Operations

### 2.1 Create and schedule events
- Define start/end windows.
- Set status lifecycle (`draft`, `scheduled`, `live`, `freeze`, `archived`).

### 2.2 Freeze windows
- Use `freeze` status when live solving should continue but ranking visibility behavior changes according to event policy.

### 2.3 Event integrity
- Event payloads are signed server-side for integrity validation.

## 3. Feature Management

### 3.1 Admin panel controls
- Feature toggles (guest preview, solver visibility, hints defaults, etc.).
- Dynamic content updates.

### 3.2 Destructive actions
- Destructive actions (e.g., delete challenge) require:
  - RBAC capability
  - CSRF token
  - `X-Admin-Confirmation` phrase

## 4. Notification Operations

- WebSocket notifications for real-time delivery.
- Email queue endpoint for outbound communication.
- Audit each admin notification action.

## 5. Audit and Compliance

### 5.1 Audit logs
- Review `/audit` for critical action traces.
- Capture actor, target, before/after (where available), and timestamp.

### 5.2 Evidence lock mode
- Enable evidence lock mode to block mutating operations during incident triage.

## 6. Operational Safety Checklist

- Rotate JWT/signing secrets periodically.
- Enable HTTPS enforcement in production.
- Keep fail2ban/firewall active on hosts.
- Validate backups and perform restore drills.
