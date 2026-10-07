ARG ODOO_IMAGE=odoo:20.0@sha256:cdd83e8359b3e8c357895d476396c05021fed9975bf420f353bab25fcaed1533
FROM ${ODOO_IMAGE}
USER root
COPY build/wkhtmltox.deb /tmp/wkhtmltox.deb
COPY build/wkhtmltox.sha256 /tmp/wkhtmltox.sha256
RUN cd /tmp && sha256sum -c wkhtmltox.sha256 \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends fonts-noto-core poppler-utils /tmp/wkhtmltox.deb \
    && wkhtmltopdf --version \
    && fc-match 'Noto Sans Myanmar' \
    && rm -rf /var/lib/apt/lists/* /tmp/wkhtmltox.deb /tmp/wkhtmltox.sha256
COPY --chown=odoo:odoo addons/ /mnt/extra-addons/
COPY scripts/bootstrap.py scripts/export_report.py scripts/verify_report.py /opt/myanmar-demo/
ENV QT_MYANMAR_HARFBUZZ=1
USER odoo
