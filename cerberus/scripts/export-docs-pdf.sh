#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOC_DIR="${ROOT_DIR}/docs"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "[!] pandoc not found. Install pandoc for PDF export."
  exit 1
fi

DOCS=(
  user-guide
  admin-guide
  challenge-author-guide
  api-reference
  deployment-maintenance-guide
  security-best-practices
)

for doc in "${DOCS[@]}"; do
  pandoc "${DOC_DIR}/${doc}.md" -o "${DOC_DIR}/${doc}.pdf"
  echo "[+] Exported ${DOC_DIR}/${doc}.pdf"
done
