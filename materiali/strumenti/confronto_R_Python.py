"""Controllo indipendente delle repliche condivise M15 e P10."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parents[1]
d=pd.read_csv(P/'dati/campioni_modulo1.csv');rho=(d.massa_g/d.volume_cm3).to_numpy()
u=pd.read_csv(P/'dati/casuali_comuni_v3.csv').u.to_numpy()
I=(np.floor(u[:240]*24).astype(int)).reshape(10,24)
y=rho[I].mean(axis=1);results=[]
for mod,file in [('M15','bootstrap_condiviso.csv'),('P10','medie_condivise.csv')]:
 r=pd.read_csv(P/f'risultati/{mod}/{file}').media.to_numpy();err=float(np.max(np.abs(r-y)))
 assert err<1e-12,(mod,err)
 results.append(dict(modulo=mod,repliche=10,errore_massimo=err,tolleranza=1e-12,esito='superato'))
(P/'verifiche/confronto_R_Python.json').write_text(json.dumps(results,indent=2));print(results)
