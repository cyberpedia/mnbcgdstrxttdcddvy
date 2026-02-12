#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pushd "${ROOT_DIR}/backend" >/dev/null
python3 -m pip install -q -r requirements.txt
pytest -q --cov=app --cov-report=term-missing --cov-report=xml:coverage.xml
ruff check app tests
bandit -q -r app
python3 -m py_compile tests/load/locustfile.py
popd >/dev/null

pushd "${ROOT_DIR}/frontend" >/dev/null
npm ci
npm run lint
npm run test
npm run build
popd >/dev/null

echo "[+] Phase 8 test suite completed"
