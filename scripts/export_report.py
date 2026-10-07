import json, os, hashlib, subprocess
from pathlib import Path
from odoo import release
out = Path('/artifacts'); out.mkdir(exist_ok=True)
partner = env.ref('myanmar_pdf_demo.partner_myanmar')
report = env.ref('myanmar_pdf_demo.action_report_myanmar')
pdf, kind = env['ir.actions.report']._render_qweb_pdf(report.id, [partner.id])
assert kind == 'pdf' and pdf.startswith(b'%PDF-')
(out / 'myanmar-demo.pdf').write_bytes(pdf)
metadata = {'odoo': release.version, 'pdf_engine': env['ir.actions.report']._get_pdf_engine(report),
            'sample': partner.name, 'expected_repetitions': 3, 'font': 'NotoSansMyanmar',
            'wkhtmltopdf': subprocess.check_output(['wkhtmltopdf','--version'],text=True).strip(),
            'binary_sha256': hashlib.sha256(Path('/usr/local/bin/wkhtmltopdf').read_bytes()).hexdigest(),
            'opt_in': os.environ.get('QT_MYANMAR_HARFBUZZ'),
            'installed_modules': env['ir.module.module'].search([('state','=','installed')]).mapped('name')}
(out / 'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
print('Demo PDF exported', len(pdf))
