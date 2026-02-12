#!/usr/bin/env sh
set -eu

if [ -n "${DB_PASSWORD_FILE:-}" ] && [ -f "${DB_PASSWORD_FILE}" ]; then
  DB_PASSWORD="$(cat "${DB_PASSWORD_FILE}")"
  export DATABASE_URL="postgresql+psycopg://${DB_USER:-cerberus_app}:${DB_PASSWORD}@${DB_HOST:-postgres}:${DB_PORT:-5432}/${DB_NAME:-cerberus}"
fi

if [ -n "${JWT_SECRET_KEY_FILE:-}" ] && [ -f "${JWT_SECRET_KEY_FILE}" ]; then
  export JWT_SECRET_KEY="$(cat "${JWT_SECRET_KEY_FILE}")"
fi

if [ -n "${SIGNING_SECRET_FILE:-}" ] && [ -f "${SIGNING_SECRET_FILE}" ]; then
  export SIGNING_SECRET="$(cat "${SIGNING_SECRET_FILE}")"
fi

exec "$@"
