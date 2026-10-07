#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, subprocess, urllib.request
parser = argparse.ArgumentParser(); parser.add_argument('--arch', choices=['arm64','amd64']); args = parser.parse_args()
root = pathlib.Path(__file__).resolve().parent.parent
arch = args.arch or subprocess.check_output(['docker','info','--format','{{.Architecture}}'],text=True).strip()
arch = {'aarch64':'arm64','x86_64':'amd64'}.get(arch,arch)
if arch not in ('arm64','amd64'): raise SystemExit('Only arm64 and amd64 packages were released')
hashes = {'arm64':'6c553e16de26e677a46f7aad51011f4c12f05cedb0b3ec0f9800f4bdce2294b5',
          'amd64':'a3877e712f5366eada334229537549015fc328e1b5337601d5b8fd216f49a143'}
url = f'https://github.com/HanZawNyein/packaging/releases/download/0.12.6.1-3-myanmar12/wkhtmltox_0.12.6.1-3.myanmar12.jammy_{arch}.deb'
folder=root/'build'; folder.mkdir(exist_ok=True); package=folder/'wkhtmltox.deb'
if not package.exists() or hashlib.sha256(package.read_bytes()).hexdigest()!=hashes[arch]:
    temp=folder/'wkhtmltox.deb.part'
    subprocess.run(['curl','--http1.1','--fail','--location','--retry','3','--connect-timeout','20','--max-time','300',url,'--output',str(temp)],check=True)
    assert hashlib.sha256(temp.read_bytes()).hexdigest()==hashes[arch], 'Release SHA256 mismatch'
    temp.replace(package)
(folder/'wkhtmltox.sha256').write_text(hashes[arch]+'  wkhtmltox.deb\n')
(folder/'release.json').write_text(json.dumps({'url':url,'sha256':hashes[arch],'architecture':arch},indent=2)+'\n')
print('Verified release package:', arch, hashes[arch])
