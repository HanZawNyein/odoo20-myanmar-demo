#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ -f .env ]] || cp .env.example .env
mkdir -p artifacts
python3 scripts/fetch-release.py
docker compose config --quiet
docker compose build odoo
docker compose up -d --wait db
# Initialize once; a second start keeps existing demo data.
if ! docker compose exec -T db psql -U odoo -tAc "SELECT 1 FROM pg_database WHERE datname='myanmar_demo'" | grep -q 1; then
  docker compose run --rm --no-deps -T odoo odoo -d myanmar_demo -i myanmar_pdf_demo --without-demo=all --stop-after-init
  docker compose run --rm --no-deps -T odoo odoo shell -d myanmar_demo --no-http < scripts/bootstrap.py
fi
docker compose up -d --wait odoo
docker compose ps
