from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import json,re,hashlib,gzip
root=Path(__file__).resolve().parents[2]
repository='https://repo.r-wasm.org/bin/emscripten/contrib/4.6/'
# Prefer the committed index to preserve the exact dependency versions.
index=root/'vendor/r-repo/bin/emscripten/contrib/4.6/PACKAGES'
raw=index.read_text() if index.exists() else urlopen(repository+'PACKAGES').read().decode()
records={};blocks={}
for block in raw.split('\n\n'):
 d={};last=None
 for ln in block.splitlines():
  if ln.startswith(' ') and last:d[last]+=' '+ln.strip()
  elif ': ' in ln:last,v=ln.split(': ',1);d[last]=v
 if 'Package'in d:records[d['Package']]=d;blocks[d['Package']]=block
base={'R','base','compiler','datasets','graphics','grDevices','grid','methods','parallel','splines','stats','stats4','tcltk','tools','utils','MASS','Matrix','mgcv','nlme','lattice','survival','boot','class','cluster','codetools','foreign','KernSmooth','nnet','rpart','spatial'}
needed=set()
def visit(name):
 if name in base or name in needed:return
 needed.add(name)
 for field in ['Depends','Imports','LinkingTo']:
  for val in records[name].get(field,'').split(','):
   dep=val.strip().split(' ')[0]
   if dep:visit(dep)
for name in ['ggplot2','jsonlite','svglite']:visit(name)
out=root/'vendor/r-repo/bin/emscripten/contrib/4.6';out.mkdir(parents=True,exist_ok=True)
def fetch(name):
 filename=records[name]['File'];p=out/filename
 if not p.exists():p.write_bytes(urlopen(Request('https://repo.r-wasm.org/bin/emscripten/contrib/4.6/'+filename,headers={'User-Agent':'GeoStatLab'}),timeout=60).read())
 b=p.read_bytes();assert hashlib.md5(b).hexdigest()==records[name]['MD5sum'],name
 return dict(package=name,version=records[name]['Version'],file=filename,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),license=records[name].get('License'))
res=list(ThreadPoolExecutor(6).map(fetch,sorted(needed)))
text='\n\n'.join(blocks[n] for n in sorted(needed))+'\n';(out/'PACKAGES').write_text(text);(out/'PACKAGES.gz').write_bytes(gzip.compress(text.encode()))
(root/'vendor/r-packages-lock.json').write_text(json.dumps(res,indent=2));print(len(res),'pacchetti',sum(x['bytes'] for x in res),'byte')
