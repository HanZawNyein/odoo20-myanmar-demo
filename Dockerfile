FROM odoo:20.0
USER root
ARG TARGETARCH
RUN set -eu; \
    WKHTMLTOPDF_ARCH="${TARGETARCH:-$(dpkg --print-architecture)}"; \
    case "$WKHTMLTOPDF_ARCH" in \
      amd64) WKHTMLTOPDF_SHA=a3877e712f5366eada334229537549015fc328e1b5337601d5b8fd216f49a143 ;; \
      arm64) WKHTMLTOPDF_SHA=6c553e16de26e677a46f7aad51011f4c12f05cedb0b3ec0f9800f4bdce2294b5 ;; \
      *) echo "Unsupported architecture: $WKHTMLTOPDF_ARCH" >&2; exit 1 ;; \
    esac; \
    curl --http1.1 --fail --location --retry 3 --connect-timeout 20 --max-time 300 \
      "https://github.com/HanZawNyein/packaging/releases/download/0.12.6.1-3-myanmar12/wkhtmltox_0.12.6.1-3.myanmar12.jammy_${WKHTMLTOPDF_ARCH}.deb" \
      --output /tmp/wkhtmltox.deb; \
    echo "$WKHTMLTOPDF_SHA  /tmp/wkhtmltox.deb" | sha256sum -c -; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends fonts-noto-core poppler-utils /tmp/wkhtmltox.deb; \
    wkhtmltopdf --version; \
    fc-match 'Noto Sans Myanmar'; \
    rm -rf /var/lib/apt/lists/* /tmp/wkhtmltox.deb
ENV QT_MYANMAR_HARFBUZZ=1
USER odoo
