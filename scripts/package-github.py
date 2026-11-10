"""Create a source-only GitHub delivery with per-file checksums. Requires Git checkout."""
from pathlib import Path
import argparse, hashlib, json, subprocess, zipfile

root = Path(__file__).resolve().parents[1]
version = json.loads((root/'package.json').read_text())['version']
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=root/f'release/GeoStatLab_GitHub_v{version}.zip')
args = parser.parse_args()
output = args.output.resolve()
output.parent.mkdir(parents=True, exist_ok=True)
files = subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=root).decode().split('\0')
excluded = {'.git','.openai','node_modules','dist','.venv','release','__pycache__'}
selected = []
for name in sorted(set(files)):
    if not name: continue
    p = Path(name)
    if any(part in excluded for part in p.parts): continue
    if name.startswith('qa/') and (p.suffix.lower() in {'.png','.jpg','.zip','.html'} or name.startswith('qa/browser/')): continue
    if p.name in {'.DS_Store','.Rhistory','.RData'} or p.name.startswith('.env'): continue
    file = root/p
    if file.is_symlink(): raise ValueError('Symlink not allowed: '+name)
    if not file.is_file(): continue
    if file.stat().st_size >= 100*1024*1024: raise ValueError('File exceeds GitHub limit: '+name)
    selected.append(name)
for required in ['README.md','SECURITY.md','DEPLOYMENT.md','.github/workflows/pages.yml','src/security.js','security/vendor-integrity.json','package-lock.json']:
    if required not in selected: raise ValueError('Missing delivery file: '+required)
commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
dirty = bool(subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip())
manifest = []
prefix = f'GeoStatLab_GitHub_v{version}/'
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
    for name in selected:
        data = (root/name).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        archive.writestr(prefix+name,data)
        manifest.append(digest+'  '+name)
    archive.writestr(prefix+'SHA256SUMS.txt','\n'.join(manifest)+'\n')
    archive.writestr(prefix+'RELEASE.json',json.dumps(dict(application='GeoStat Lab',version=version,source_commit=commit,working_tree_modified=dirty,files=len(selected),checksums='SHA256SUMS.txt',excluded=['Git metadata','private hosting identifiers','node_modules','dist','browser sessions and screenshots']),ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(output) as archive:
    if archive.testzip() is not None: raise ValueError('Archive CRC verification failed')
    for line in manifest:
        digest,name=line.split('  ',1)
        if hashlib.sha256(archive.read(prefix+name)).hexdigest()!=digest: raise ValueError('Archive checksum mismatch: '+name)
sha=hashlib.sha256(output.read_bytes()).hexdigest()
output.with_suffix(output.suffix+'.sha256').write_text(sha+'  '+output.name+'\n')
print(json.dumps(dict(path=str(output),bytes=output.stat().st_size,sha256=sha,files=len(selected),source_commit=commit,working_tree_modified=dirty)))
