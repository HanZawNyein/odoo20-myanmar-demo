# Odoo 20 with Myanmar wkhtmltopdf

Uses `FROM odoo:20.0` with the released Myanmar wkhtmltopdf package. The Compose layout follows the official Odoo Docker example: `web`, PostgreSQL 16, a password secret, mounted configuration/addons and persistent volumes.

## Start a new instance

Create `odoo_pg_pass` containing the PostgreSQL password (one line). This file is ignored by Git and excluded from the image build context. Both services read the same secret; the password is not stored in Compose.

```bash
printf '%s\n' 'local-demo-db' > odoo_pg_pass
docker compose build
docker compose up -d
```

Open http://localhost:8069. On a fresh database volume, create your Odoo database through the database manager and select your login/password. For a reproducible local `myanmar_demo` database with `admin` / `admin`, initialize it instead before starting `web`:

```bash
docker compose up -d db
docker compose run --rm -T web odoo -d myanmar_demo -i base,web,base_report_wkhtmltox --without-demo=all --stop-after-init
docker compose up -d web
```

For wkhtmltopdf reports, install the official `base_report_wkhtmltox` addon if it is not already installed. Select the renderer and internal asset URL for that database:

```bash
docker compose exec -T web /entrypoint.sh odoo shell -d myanmar_demo --no-http <<'PY'
params = env['ir.config_parameter'].sudo()
params.set_str('report.pdf_engine_default', 'wkhtmltopdf')
params.set_str('report.url', 'http://web:8069')
env.cr.commit()
PY
```

Use standard Odoo apps/reports. `addons/` is empty; no custom module or helper scripts are included. `config/odoo.conf` preserves the official addons/data paths. PostgreSQL credentials come from the secret through the official entrypoint.

## Release

The Dockerfile determines architecture using `dpkg --print-architecture`, downloads the released ARM64/AMD64 `.deb` directly, verifies SHA256 and installs it. It reuses tools/libraries from the base and adds Noto Myanmar fonts (`fonts-noto-core`). `QT_MYANMAR_HARFBUZZ=1` enables the new shaping path.

- [wkhtmltopdf release](https://github.com/HanZawNyein/packaging/releases/tag/0.12.6.1-3-myanmar12)
- [Source changes and patches](docs/wkhtmltopdf-changes.md)
- [Historical report verification](docs/verification.md)
- [Official Odoo Docker reference](https://github.com/odoo/docker)

## Existing demo / persistence

This new Compose definition uses port 8069, service `web` and volumes `odoo-web-data` / `odoo-db-data`. The earlier running demo used port 8070, service `odoo` and different volumes. Editing this file does not migrate that database or stop its running containers. The new definition has been validated but has not been deployed over the existing demo. Migrate the database/filestore explicitly if you need its data in this new layout.

```bash
docker compose stop
docker compose down
```

These preserve named volumes. `down -v` deletes the selected project's data. Changing `odoo_pg_pass` does not change an already initialized PostgreSQL role's password. The original demo's admin/admin credentials remain on its existing database; a new volume has its own database setup.
