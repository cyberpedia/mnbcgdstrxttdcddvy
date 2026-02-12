# Phase 8 Testing Guide

## Scope

- Unit tests: backend utils/services/models behavior
- Integration tests: API endpoints + RBAC workflows
- E2E/UI tests: React Testing Library workflows
- Security tests: XSS, SQLi-style payloads, CSRF, auth bypass
- Load tests: leaderboard, notifications, multi-challenge flows

## Backend commands

```bash
cd cerberus/backend
pip install -r requirements.txt
pytest -q --cov=app --cov-report=term-missing --cov-report=xml:coverage.xml
```

Test files include:
- `tests/test_unit_utils.py`
- `tests/test_unit_services.py`
- `tests/test_integration_rbac.py`
- `tests/test_security_cases.py`
- `tests/test_api.py`

## Frontend commands

```bash
cd cerberus/frontend
npm ci
npm run test
```

React Testing Library tests live in:
- `src/test/app.test.jsx`
- `src/test/admin-panel.test.jsx`
- `src/test/challenge-page.test.jsx`

Coverage outputs under `cerberus/frontend/coverage/`.

## Load testing

```bash
locust -f cerberus/backend/tests/load/locustfile.py --host http://127.0.0.1:8000
```

## CI coverage

`security-quality.yml` publishes coverage artifacts:
- backend: `coverage.xml`
- frontend: `coverage/`
