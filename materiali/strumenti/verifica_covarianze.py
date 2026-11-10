"""Confronto indipendente con statsmodels delle covarianze R di P03–P05."""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_hac
import json
P=Path(__file__).resolve().parents[1]
results=[]
for mod in ['P03','P04','P05']:
 if mod=='P03':
  d=pd.read_csv(P/'dati/progetti/nile.csv'); X=sm.add_constant((d.year>=1898).astype(float));y=d.volume_1e8_m3;lag=3;typ='HAC'
 elif mod=='P04':
  d=pd.read_csv(P/'dati/progetti/faithful.csv').merge(pd.read_csv(P/'dati/progetti/piani_ricampionamento/faithful_split.csv'),on='row_id').query("set=='train'")
  X=sm.add_constant(d.eruption_min);y=d.waiting_min;typ='HC3'
 else:
  d=pd.read_csv(P/'risultati/P05/mensile_modelli.csv');X=sm.add_constant(pd.concat([d[['t']],pd.get_dummies(d.month,prefix='mese',drop_first=True,dtype=float)],axis=1));y=d.co2_ppm;lag=12;typ='HAC'
 f=sm.OLS(y,X).fit();V=cov_hac(f,nlags=lag,use_correction=True) if typ=='HAC' else f.cov_HC3
 R=pd.read_csv(P/f'risultati/{mod}/cov_{typ}.csv').to_numpy()
 err=float(np.max(np.abs(R-np.asarray(V))));ok=bool(np.allclose(R,V,rtol=1e-9,atol=1e-10));assert ok,(mod,err)
 results.append(dict(progetto=mod,covarianza=typ,errore_massimo=err,esito=ok))
(P/'verifiche/confronto_covarianze.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
