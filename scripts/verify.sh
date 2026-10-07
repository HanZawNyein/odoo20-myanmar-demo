#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose exec -T odoo /entrypoint.sh odoo shell -d myanmar_demo --no-http < scripts/export_report.py
docker compose logs --no-color odoo > artifacts/server.log
docker compose exec -T odoo python3 /opt/myanmar-demo/verify_report.py
