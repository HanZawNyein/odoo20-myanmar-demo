import hashlib,json,pathlib,re,subprocess
out=pathlib.Path('/artifacts'); m=json.loads((out/'metadata.json').read_text())
norm=lambda t: ''.join(t.split())
r=subprocess.run(['pdftotext','-enc','UTF-8',str(out/'myanmar-demo.pdf'),'-'],capture_output=True,text=True,check=True)
assert 'Syntax Error' not in r.stderr, r.stderr
(out/'myanmar-demo.txt').write_text(r.stdout)
info=subprocess.check_output(['pdfinfo',str(out/'myanmar-demo.pdf')],text=True)
fonts=subprocess.check_output(['pdffonts',str(out/'myanmar-demo.pdf')],text=True)
(out/'pdfinfo.txt').write_text(info);(out/'pdffonts.txt').write_text(fonts)
column=fonts.splitlines()[0].index('emb')
embedded=any('NotoSansMyanmar' in line and line[column:column+3]=='yes' for line in fonts.splitlines()[2:])
assets=[line for line in (out/'server.log').read_text().splitlines() if 'GET /web/assets/' in line]
results={'odoo_20':m['odoo'].startswith('20.0'),'wkhtmltopdf_engine':m['pdf_engine']=='wkhtmltopdf',
'opt_in':m['opt_in']=='1','binary_matches_release':m['binary_sha256'] in ('9993b76cace04b56a21e8de7a7a5e9ec176ac6232a5606916c0e3adaf54d4ea1','5ebb334a40935f63329d59e614c69afd6514722e7ecfb176d9feedfb3d8eb759'),
'exact_unicode_repetitions':norm(r.stdout).count(norm(m['sample'])),'two_pages':bool(re.search(r'Pages:\s+2\b',info)),
'footers':all(f'Page{i}/2' in norm(r.stdout) for i in (1,2)), 'font_embedded':embedded,
'live_assets':len(assets)>=2 and all(' 200 ' in line for line in assets),
'no_pua_workaround':not any('ReportMyanmarText' in n or 'report_myanmar_text' in n for n in m['installed_modules'])}
passed=results['exact_unicode_repetitions']==3 and all(v for k,v in results.items() if k!='exact_unicode_repetitions')
results['passed']=passed;(out/'verification.json').write_text(json.dumps(results,indent=2)+'\n')
subprocess.run(['pdftoppm','-png','-r','96',str(out/'myanmar-demo.pdf'),str(out/'myanmar-demo')],capture_output=True,check=True)
print(json.dumps(results,indent=2));assert passed
