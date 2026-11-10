"""Controllo della struttura della consegna e dei resoconti di collaudo."""
from pathlib import Path
import json,hashlib,re,csv
import fitz
P=Path(__file__).resolve().parents[1]
def read(f):return json.loads((P/f).read_text())
mods=read('documentazione/indice_corso.json');checks=[]
for m in mods:
 id=m['id'];data=read(f'sorgenti/contenuti/{id}.json');assert len(data['pagine'])+2==m['pagine']
 with fitz.open(P/m['pdf']) as doc:
  assert len(doc)==m['pagine']
  assert all(abs(p.rect.width-566.929)<.1 and abs(p.rect.height-354.331)<.1 for p in doc)
  assert all('[[' not in p.get_text() for p in doc)
 for s in data['pagine']:
  for key,folder,ext in [('figura','figure','.pdf'),('tikz','tikz','.tex'),('codice','estratti','.R')]:
   if s[key]:assert (P/folder/(s[key]+ext)).is_file(),(id,key,s[key])
 metrics=read(f'verifiche/{id}/geometria.json');assert len(metrics)==len(data['pagine'])*4 and all(x['ok'] for x in metrics)
 log=(P/f'verifiche/{id}/{id}_R6.log').read_text(errors='replace');assert 'Overfull' not in log and 'Missing character:' not in log
 checks.append(dict(modulo=id,pagine=m['pagine'],esito='superato'))
assert len(mods)==28 and sum(m['pagine'] for m in mods)==861
for x in read('verifiche/esecuzione_laboratori.json'):
 assert x['exit_code']==0 and hashlib.sha256((P/x['script']).read_bytes()).hexdigest()==x['sha256']
assert len(read('verifiche/esecuzione_laboratori.json'))==340
for x in read('verifiche/estratti/esito.json'):
 assert x['exit_code']==0 and hashlib.sha256((P/x['estratto']).read_bytes()).hexdigest()==x['sha256']
assert len(read('verifiche/estratti/esito.json'))==108
for x in read('verifiche/python_T00/esito.json'):
 assert x['esito']==0 and hashlib.sha256((P/x['file']).read_bytes()).hexdigest()==x['sha256']
rows=list(csv.DictReader((P/'documentazione/raccordo_slide.csv').open()));assert len(rows)==2150 and all(x['pagine_R6'] for x in rows)
bad=[]
for f in (P/'figure').glob('*/*.pdf'):
 with fitz.open(f) as doc:
  p=doc[0]
  for b in p.get_text('dict')['blocks']:
   for l in b.get('lines',[]):
    for s in l['spans']:
     x,y,xx,yy=s['bbox']
     if min(x,y)<-.5 or xx>p.rect.width+.5 or yy>p.rect.height+.5:bad.append((str(f),s['text']))
assert not bad,bad
for name in ['Guida_corso_R6','Guida_laboratori_M05']:
 with fitz.open(P/f'{name}.pdf') as d:assert all(not re.search(r'\[\[\w+\]\]',p.get_text()) for p in d)
for x in read('documentazione/catalogo_laboratori.json'):
 assert hashlib.sha256((P/x['script']).read_bytes()).hexdigest()==x['sha256']
audit=read('audit/registro.json');assert len(audit)==861
assert {(x['modulo'],x['pagina']) for x in audit}=={(m['id'],i) for m in mods for i in range(1,m['pagine']+1)}
assert all(x['stato'] in ['verificata','verificata dopo correzione'] for x in audit)
assert sum(x['stato']=='verificata dopo correzione' for x in audit)==357
assert (P/'audit/Rapporto_revisione_R6.pdf').is_file() and (P/'audit/Registro_slide_R6.html').is_file()
result=dict(esito='superato',slide_rilette=861,slide_corrette=357,fascicoli=checks,laboratori_R=340,estratti_R=108,laboratori_Python=20,raccordi_originali=2150,figure_fuori_pagina=0)
(P/'verifiche/consegna_finale.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('CONSEGNA VERIFICATA: 28 fascicoli, 861 slide, 340 laboratori R, 108 estratti, 20 laboratori Python.')
