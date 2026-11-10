"""Importa i contenuti R6 e genera le rappresentazioni vettoriali delle slide."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,subprocess,re
ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT/'materiali'
args=argparse.ArgumentParser()
args.add_argument('--render',action='store_true',help='Rigenera tutte le slide SVG dai PDF approvati.')
args=args.parse_args()
index=json.loads((COURSE/'documentazione/indice_corso.json').read_text())
labs=json.loads((COURSE/'documentazione/catalogo_laboratori.json').read_text())
audit=json.loads((COURSE/'audit/registro.json').read_text())
catalogue=[]
for i,m in enumerate(index):
 mid=m['id'];data=json.loads((COURSE/f'sorgenti/contenuti/{mid}.json').read_text())
 rows=[r for r in audit if r['modulo']==mid]
 sections=[]
 pages=[dict(page=1,title=data['titolo'],section='Apertura',body=data['sottotitolo'],kind='copertina'),
        dict(page=2,title='Percorso del modulo',section='Apertura',body='L’indice presenta le sezioni del fascicolo e le relative pagine iniziali.',kind='indice')]
 for n,s in enumerate(data['pagine'],3):
  if not sections or sections[-1]['title']!=s['sezione']:sections.append(dict(title=s['sezione'],page=n))
  pages.append(dict(page=n,title=s['titolo'],section=s['sezione'],body=s['testo'],aside=s['destra'],formula=s['formula'],formulaAside=s['formula_destra'],caption=s['didascalia'],recall=s['richiamo'],sources=s['fonti'],origin=s['origine'],kind='contenuto',figure=s['figura'],diagram=s['tikz'],codePath=f"materiali/estratti/{s['codice']}.R" if s['codice'] else '',code=(COURSE/f"estratti/{s['codice']}.R").read_text() if s['codice'] else ''))
 for page in pages:
  page['image']=f"assets/slides/{mid}/{page['page']:03}.svg"
  row=rows[page['page']-1];page['review']=dict(observation=row['osservazioni'],intervention=row['intervento'],status=row['stato'])
 mlabs=[dict(id=x['id'],title=x['titolo'],path='materiali/'+x['script'],sha256=x['sha256'],language='Python' if x['script'].endswith('.py') else 'R') for x in labs if x['modulo']==mid]
 if mid=='T00':
  for x in json.loads((COURSE/'verifiche/python_T00/esito.json').read_text()):
   f=COURSE/x['file'];title=f.read_text().splitlines()[0].lstrip('# ').strip()
   mlabs.append(dict(id=f.stem.replace('T00_','T00_PY_'),title=title,path='materiali/'+x['file'],sha256=x['sha256'],language='Python'))
 for x in mlabs:x['code']=(ROOT/x['path']).read_text()
 script=f'materiali/R/{mid}_figure.R'
 item=dict(id=mid,title=data['titolo'],subtitle=data['sottotitolo'],category='progetti' if mid.startswith('P') else 'moduli',pages=m['pagine'],figures=m['figure'],diagrams=m['tikz'],formulas=m['formule'],pdf=f"materiali/pdf/{mid}_R6.pdf",sections=sections,labs=len(mlabs),previous=index[i-1]['id'] if i else None,next=index[i+1]['id'] if i+1<len(index) else None,script=script,preview=f'assets/slides/{mid}/001.svg')
 item['keywords']=[s['titolo'] for s in data['pagine']]
 catalogue.append(item)
 bundle=dict(**item,slides=pages,laboratories=mlabs,figureCode=(ROOT/script).read_text(),source=f'materiali/sorgenti/{mid}.py',tex=f'materiali/sorgenti/{mid}_R6.tex')
 folder=ROOT/f'moduli/{mid}';folder.mkdir(parents=True,exist_ok=True)
 (folder/'modulo.json').write_text(json.dumps(bundle,ensure_ascii=False,indent=2))
 md=f"# {mid} · {data['titolo']}\n\n{data['sottotitolo']}.\n\n**{m['pagine']} slide · {m['figure']} figure · {m['tikz']} diagrammi TikZ · {len(mlabs)} laboratori.**\n\n"
 md+=f"[PDF del modulo](../../{item['pdf']}) · [Codice R delle figure](../../{script}) · [Sorgente LaTeX](../../{bundle['tex']}) · [Indice del repository](../../README.md)\n\n## Percorso\n\n"
 md+=''.join(f"- Pagina {s['page']}: {s['title']}.\n" for s in sections)
 md+="\n## Esecuzione\n\nAprire §materiali/Corso_Geologia.Rproj§, oppure avviare R nella cartella §materiali/§, quindi eseguire:\n\n"
 md+='§§§r\nsource("R/'+mid+'_figure.R")\n§§§\n\n'
 md+="Le dipendenze comuni e i dati restano nella cartella §materiali/§; scaricare l’intero repository prima di eseguire gli script.\n\n"
 if mlabs:
  md+="## Laboratori\n\n| Codice | Attività | File |\n|---|---|---|\n"
  md+=''.join(f"| {x['id']} | {x['title']} | [{x['language']}](../../{x['path']}) |\n" for x in mlabs)
 md+="\n## Tracciabilità\n\nLa numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). §modulo.json§ raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.\n"
 (folder/'README.md').write_text(md.replace('§',chr(96)))
(ROOT/'content/catalogue.json').write_text(json.dumps(dict(version='1.0.0',edition='R6',modules=catalogue),ensure_ascii=False,indent=2))
(ROOT/'content/origin.json').write_text(json.dumps(dict(course='Geologia_Corso_R6',edition='R6',slides=861,referenceRepository='https://github.com/marzione00/QuantumLab_Public',referenceCommit='275b07805da69af75ba6c2f64ea0ba99ae4144ea',sourceManifestSHA256=hashlib.sha256((COURSE/'MANIFEST_SHA256.txt').read_bytes()).hexdigest(),note='Architettura autonoma ispirata al repository di riferimento; interfaccia e strumenti di build realizzati per questo corso.'),ensure_ascii=False,indent=2))
if args.render:
 def render(m):
  folder=ROOT/f"assets/slides/{m['id']}";folder.mkdir(parents=True,exist_ok=True)
  for n in range(1,m['pages']+1):
   subprocess.run(['pdftocairo','-svg','-f',str(n),'-l',str(n),str(ROOT/m['pdf']),str(folder/f'{n:03}.svg')],check=True,capture_output=True)
  return m['id']
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  for mid in pool.map(render,catalogue):print(mid,'slide vettoriali generate',flush=True)
for m in catalogue:
 data=json.loads((ROOT/f"moduli/{m['id']}/modulo.json").read_text())
 folder=ROOT/f"assets/visuals/{m['id']}";folder.mkdir(parents=True,exist_ok=True)
 for s in data['slides']:
  if not(s.get('figure') or s.get('diagram')):continue
  target=folder/f"{s['page']:03}.svg"
  if s.get('figure'):
   if args.render or not target.exists():
    subprocess.run(['pdftocairo','-svg',str(COURSE/f"figure/{s['figure']}.pdf"),str(target)],check=True,capture_output=True)
   continue
  source=ROOT/s['image']
  if not source.exists():continue
  text=source.read_text()
  text=re.sub(r'(<svg[^>]*?)width="[^"]*"',r'\1width="211.181pt"',text,count=1)
  text=re.sub(r'(<svg[^>]*?)height="[^"]*"',r'\1height="212.598pt"',text,count=1)
  text=re.sub(r'viewBox="[^"]*"','viewBox="328.819 77.953 211.181 212.598"',text,count=1)
  target.write_text(text)
print('Importati',len(catalogue),'fascicoli;',sum(m['pages'] for m in catalogue),'slide.',flush=True)

# Keep module documentation aligned with the interactive catalogue.
subprocess.run(['node','scripts/update-module-guides.mjs'],cwd=ROOT,check=True)
