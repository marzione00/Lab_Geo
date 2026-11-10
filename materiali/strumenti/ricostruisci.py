"""Eseguire dalla radice: python strumenti/ricostruisci.py --help."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,os,shutil,subprocess,sys,time
P=Path(__file__).resolve().parents[1];os.chdir(P)
a=argparse.ArgumentParser();a.add_argument('azione',choices=['figure','slide','laboratori','estratti','python','tutto']);a.add_argument('moduli',nargs='*');a.add_argument('--r-bin',default=os.environ.get('R_BIN','R'));a.add_argument('--jobs',type=int,default=4);args=a.parse_args()
mods=args.moduli or ['T00']+[f'M{i:02}' for i in range(1,17)]+[f'P{i:02}' for i in range(1,12)]
logs=P/'verifiche/riesecuzione';logs.mkdir(exist_ok=True,parents=True)
def rrun(expr):return [args.r_bin,'--vanilla','--slave','-e',expr]
def execute(item):
 name,cmd,src=item;t=time.time();q=subprocess.run(cmd,cwd=P,env=dict(os.environ,MPLBACKEND='Agg'),capture_output=True,text=True,timeout=600)
 (logs/(name+'.log')).write_text(q.stdout+q.stderr)
 return dict(id=name,exit_code=q.returncode,secondi=round(time.time()-t,3),sorgente=src,sha256=hashlib.sha256((P/src).read_bytes()).hexdigest() if src else '')
def batch(kind,items):
 with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,args.jobs)) as pool:out=list(pool.map(execute,items))
 (logs/(kind+'.json')).write_text(json.dumps(out,indent=2));bad=[x['id'] for x in out if x['exit_code']];print(kind,len(out)-len(bad),'/',len(out),flush=True)
 if bad:raise RuntimeError('Controllare i log: '+', '.join(bad))
for action in (['figure','slide','laboratori','estratti','python'] if args.azione=='tutto' else [args.azione]):
 if action=='figure':
  q=subprocess.run(rrun("source('R/controlla_ambiente.R')"),check=True)
  # Ogni processo produce file soltanto nella cartella del proprio modulo.
  batch(action,[(m,rrun(f"source('R/{m}_figure.R')"),f'R/{m}_figure.R') for m in mods])
 elif action=='slide':
  if not shutil.which('xelatex'):raise RuntimeError('Installare XeLaTeX con Beamer, TikZ, fontspec, listings e bookmark.')
  for m in mods:
   subprocess.run([sys.executable,f'sorgenti/{m}.py'],check=True)
   subprocess.run([sys.executable,'sorgenti/compila.py',m],check=True)
 elif action in ['laboratori','estratti']:
  items=[]
  for f in sorted((P/action).glob('*/*.R')):
   if f.parent.name not in mods:continue
   rel=f.relative_to(P).as_posix();name=f.parent.name+'_'+f.stem
   ctx="source('R/M05/calcoli.R');source('R/M05/figure.R');" if action=='estratti' and f.parent.name=='M05' else ''
   expr=ctx+f"pdf('verifiche/riesecuzione/{name}.pdf');source('{rel}');dev.off()"
   items.append((name,rrun(expr),rel))
  batch(action,items)
 else:
  items=[(f.stem,[sys.executable,str(f)],f.relative_to(P).as_posix()) for f in sorted((P/'laboratori_python').glob('*/*.py')) if f.parent.name in mods]
  batch(action,items)
  for f in ['confronto_R_Python.py','verifica_covarianze.py']:subprocess.run([sys.executable,str(P/'strumenti'/f)],check=True)
