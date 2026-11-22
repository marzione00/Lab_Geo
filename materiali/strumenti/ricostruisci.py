"""Eseguire dalla radice: python strumenti/ricostruisci.py --help."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,os,shutil,subprocess,sys,time
P=Path(__file__).resolve().parents[1];os.chdir(P)
a=argparse.ArgumentParser();a.add_argument('azione',choices=['laboratori','python','tutto']);a.add_argument('moduli',nargs='*');a.add_argument('--r-bin',default=os.environ.get('R_BIN','R'));a.add_argument('--jobs',type=int,default=4);args=a.parse_args()
mods=args.moduli or ['T00']+[f'M{i:02}' for i in range(1,17)]
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
for action in (['laboratori','python'] if args.azione=='tutto' else [args.azione]):
 if action=='laboratori':
  subprocess.run(rrun("source('R/controlla_ambiente.R')"),check=True)
  items=[]
  for f in sorted((P/action).glob('*/*.R')):
   if f.parent.name not in mods:continue
   rel=f.relative_to(P).as_posix();name=f.parent.name+'_'+f.stem
   items.append((name,rrun(f"pdf('verifiche/riesecuzione/{name}.pdf');source('{rel}');dev.off()"),rel))
  batch(action,items)
 else:
  items=[(f.stem,[sys.executable,str(f)],f.relative_to(P).as_posix()) for f in sorted((P/'laboratori_python').glob('*/*.py')) if f.parent.name in mods]
  batch(action,items)
  subprocess.run([sys.executable,str(P/'strumenti'/'confronto_R_Python.py')],check=True)
