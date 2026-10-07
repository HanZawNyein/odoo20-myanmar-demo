# Running demo verification

Verified on 2026-10-08 (Asia/Yangon) using Docker Desktop Linux ARM64 on macOS.

- Odoo: `20.0-20260926`, official image pinned in the Dockerfile.
- Package: `1:0.12.6.1-3.myanmar12.jammy` from the public GitHub release URL.
- Renderer: `wkhtmltopdf 0.12.6.1 (with patched qt)`; engine `wkhtmltopdf` with `QT_MYANMAR_HARFBUZZ=1`.
- Installed binary SHA256: `9993b76cace04b56a21e8de7a7a5e9ec176ac6232a5606916c0e3adaf54d4ea1` (matches the released ARM64 binary).
- Font: Ubuntu `fonts-noto-core` 20201225-2 / Noto Sans Myanmar.
- Runtime HarfBuzz: 8.3.0-2build2 on Ubuntu Noble.
- PostgreSQL and Odoo containers: healthy. Local port: `127.0.0.1:8070`.

`./scripts/verify.sh` passed: original Unicode sentence extracted three times; two PDF pages; both page footers; embedded Myanmar font; live HTTP 200 report assets; correct released binary and chosen PDF engine; no ReportMyanmarText workaround module.

The sample addon only registers QWeb report templates, menus and a contact containing the original text. It does not change text or renderer internals.

- [Sample PDF](demo-report.pdf)
- [Page 1](demo-report-page-1.png) / [Page 2](demo-report-page-2.png)
- [Machine-readable results](verification.json)
- [Runtime metadata](runtime-metadata.json)

The PDF previews were visually inspected. Browser automation could not open localhost because its admin policy check was unavailable; UI clicks were not verified. Open the running local URL manually and use the report instructions in the README. The report itself was generated through Odoo's real QWeb/wkhtmltopdf pipeline and fetched assets from its live server.

The new runtime demo was tested on ARM64. AMD64 release packages were previously tested in the renderer project, but this new Odoo demo was not run on AMD64. The exported sample can wrap within words; modern Myanmar word-breaking remains outside this patch's scope.

## Direct release download in Dockerfile

The image was rebuilt and the running demo reverified after replacing local package COPY with an architecture-specific GitHub release download inside the Dockerfile. The ARM64 download passed SHA256 verification; all QWeb PDF checks above passed again. `build/` is excluded from the Docker build context and the host fetch helper was removed.
