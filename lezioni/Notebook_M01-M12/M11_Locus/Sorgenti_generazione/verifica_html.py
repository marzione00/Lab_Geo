from pathlib import Path
from html.parser import HTMLParser
import csv,json,hashlib,urllib.parse
HERE=Path(__file__).resolve().parent
BASE=HERE.parent if HERE.name=='Sorgenti_generazione' else HERE.parent/'M11/03_Notebook_svolti/M11_Locus'
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
errors=[];checks=[]
for p in sorted(BASE.glob('*.html')):
 start_errors=len(errors)
 s=p.read_text(); tree=Audit();tree.feed(s);ids={a['id'] for t,a in tree.tags if 'id' in a}
 for tag,attrs in tree.tags:
  href=attrs.get('href')
  if href:
   u=urllib.parse.urlparse(href)
   if not u.scheme and not href.startswith('//'):
    if not u.path and u.fragment and u.fragment not in ids:errors.append([p.name,'missing anchor',href])
    if u.path and not (p.parent/urllib.parse.unquote(u.path)).exists():errors.append([p.name,'missing file',href])
  if 'src' in attrs and not attrs['src'].startswith('data:'):errors.append([p.name,'not embedded src',attrs['src']])
  if tag=='script' or (tag=='link' and attrs.get('rel')=='stylesheet'):errors.append([p.name,'external runtime risk'])
 if '@import' in s:errors.append([p.name,'CSS import'])
 if any(ord(c)<32 and c not in '\n\r\t' for c in s):errors.append([p.name,'control chars'])
 checks.append({'file':p.name,'images':sum(t=='img' for t,a in tree.tags),'mathml':sum(t=='math' for t,a in tree.tags),'links':sum('href' in a for t,a in tree.tags),'esito':'OK' if len(errors)==start_errors else 'ERRORE'})
for r in csv.DictReader((BASE/'VERIFICA_NOTEBOOK.csv').open()):
 for field,key in [('rmd','sha256_Rmd'),('html','sha256_HTML')]:
  if hashlib.sha256((BASE/r[field]).read_bytes()).hexdigest()!=r[key]:errors.append([r['id'],'hash mismatch',field])
for r in csv.DictReader((BASE/'MAPPA_ORIGINALI.csv').open()):
 if hashlib.sha256((BASE/r['svolgimento']).read_bytes()).hexdigest()!=r['sha256_svolgimento']:errors.append([r['id'],'original mapping Rmd hash mismatch'])
 if hashlib.sha256((BASE/r['originale']).read_bytes()).hexdigest()!=r['sha256_originale']:errors.append([r['id'],'original source hash mismatch'])
print('Offline checks',len(checks),'errors',len(errors));print(errors)
(BASE/'Verifiche/audit_html_offline.json').write_text(json.dumps({'controlli':checks,'errori':errors},ensure_ascii=False,indent=2))
assert not errors
