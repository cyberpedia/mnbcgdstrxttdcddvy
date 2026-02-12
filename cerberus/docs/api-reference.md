# Cerberus API Reference

> Base URL: `https://<host>/api` (reverse-proxied) or backend direct `http://<host>:8000`

## Authentication

### `POST /auth/register`
Register user.

Request:
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "VeryStrongPassword123!",
  "role": "user"
}
```

### `POST /auth/login`
Returns access/refresh + CSRF token.

### `POST /auth/refresh`
Refreshes access token.

## Events

### `POST /events`
Create event. Requires `manage_events`.

### `POST /events/{event_id}/status`
Update event state.

## Challenges

### `POST /challenges`
Create challenge. Requires `manage_challenges`.

### `PATCH /challenges/{challenge_id}`
Update challenge.

### `DELETE /challenges/{challenge_id}`
Delete challenge.

Headers required:
- `Authorization: Bearer <token>`
- `X-CSRF-Token: <token>`
- `X-Admin-Confirmation: CONFIRM-DESTRUCTIVE`

### `POST /challenges/{challenge_id}/sub-challenges`
Create challenge part.

### `POST /challenges/{challenge_id}/hints`
Add hint.

### `POST /challenges/hints/{hint_id}/toggle?enabled=true|false`
Enable or disable hint.

## Leaderboard

### `POST /leaderboard/submit`
Submit a flag.

Query params:
- `event_id`
- `challenge_id`
- `flag`
- optional `sub_challenge_id`

### `GET /leaderboard/{event_id}`
Returns signed leaderboard payload:
```json
{
  "event_id": 1,
  "rows": [{"user_id": 4, "score": 200}],
  "signature": "<hmac-sha256>"
}
```

## Notifications

### `POST /notifications/ws-send`
Send real-time notification.

### `POST /notifications/email`
Queue email notification.

### `GET/WS /notifications/ws/{user_id}`
WebSocket stream endpoint.

## UI Config

### `PUT /ui-config`
Update dynamic UI config.

### `GET /ui-config`
Read UI config.

## Audit

### `GET /audit`
Read audit logs (RBAC-gated).

## File Security

### `POST /files/verify`
Validate file hash and perform antivirus check.

Request:
```json
{
  "path": "/tmp/sample.bin",
  "expected_sha256": "<64-char-hex>"
}
```

Response:
```json
{
  "hash_valid": true,
  "antivirus": {"engine": "stub", "status": "clean"}
}
```
