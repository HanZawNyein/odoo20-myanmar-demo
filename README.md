# Odoo 20 Myanmar PDF demo

Runs the official Odoo 20 Community image with the released Myanmar Unicode wkhtmltopdf renderer. PostgreSQL and Odoo have dedicated persistent volumes. The web server binds only to `127.0.0.1:8070`.

```bash
cp .env.example .env
mkdir -p artifacts
docker compose build
docker compose up -d --wait db
# Run once for a fresh database:
docker compose run --rm --no-deps -T odoo odoo -d myanmar_demo -i myanmar_pdf_demo --without-demo=all --stop-after-init
docker compose up -d --wait
```

For a new database, select wkhtmltopdf and the internal report URL once:

```bash
docker compose exec -T odoo /entrypoint.sh odoo shell -d myanmar_demo --no-http <<'PY'
params = env['ir.config_parameter'].sudo()
params.set_str('report.pdf_engine_default', 'wkhtmltopdf')
params.set_str('report.url', 'http://odoo:8069')
env.cr.commit()
PY
```

For the already initialized demo, simply run `docker compose up -d --wait`.

Open http://localhost:8070 and sign in with `admin` / `admin`. These are disposable local demo credentials. Change the password in Odoo before using this setup beyond the local demo.

Open **Myanmar PDF Demo → Unicode sample**, open/select the sample contact, then choose **Print → Myanmar Unicode Demo**. The two-page QWeb PDF repeats the original Unicode sentence three times with a table and page footers. The addon only supplies report/menu/sample data; it performs no text reordering or PUA conversion.

The previously verified sample PDF, previews and results are committed under `docs/`. Print a fresh report through Odoo to test the current runtime.

## Image and release

- Official base: `FROM odoo:20.0`. The demo was verified with Odoo 20.0-20260926.
- PostgreSQL: 16 Alpine, pinned digest in Compose.
- Release: [0.12.6.1-3-myanmar12](https://github.com/HanZawNyein/packaging/releases/tag/0.12.6.1-3-myanmar12).
- The Dockerfile downloads the public `.deb` directly from the GitHub release URL, selects ARM64/AMD64 via `TARGETARCH` (with a dpkg fallback), and verifies its pinned SHA256. No local package file or source build is used.
- The Dockerfile installs that package with apt (including `libharfbuzz0b`), `fonts-noto-core` and PDF inspection tools, then returns to the official `odoo` user.
- `QT_MYANMAR_HARFBUZZ=1` enables the new path. A complete Unicode Myanmar font is required.

ARM64 and AMD64 are supported. The initial running demo is ARM64 on Docker Desktop/macOS. This does not validate a macOS-native renderer. Docker BuildKit selects the package for the target architecture automatically. Build/run with a matching Docker platform when cross-building. The Jammy package is used on the official Odoo image's Ubuntu Noble base, matching the upstream package choice; apt resolves the runtime libraries.

## Restart / stop

```bash
docker compose up -d --wait
docker compose stop
docker compose down
```

These preserve database and filestore volumes. Do not use `down -v` unless you intend to delete the demo data. Only run the initialization command for a new database. Change an existing user's password in Odoo.

See [wkhtmltopdf source changes](docs/wkhtmltopdf-changes.md) and [verification results](docs/verification.md).

## References

The layout follows the [official Odoo Docker Hub guide](https://hub.docker.com/_/odoo): PostgreSQL, `/var/lib/odoo` persistence, official connection variables, and `/mnt/extra-addons`. The [official Odoo 20 Dockerfile](https://github.com/odoo/docker/blob/master/20.0/Dockerfile) selects the same upstream Jammy wkhtmltopdf packaging family. This demo inherits the official entrypoint and Odoo configuration.

The release is published as a normal GitHub release. Its Myanmar implementation remains opt-in and has known limits; a release label does not expand the tested font/style/bidi coverage. Read the change document before using it for production reports.
