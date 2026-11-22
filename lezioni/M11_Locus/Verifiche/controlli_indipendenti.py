"""Controlli indipendenti dei risultati R M11.
Usa NumPy/SciPy/pandas e pyproj; nessun risultato Python rimpiazza gli output R.
Dalla radice modulo: python Verifiche/controlli_indipendenti.py
"""
from pathlib import Path
import json, hashlib, itertools, sys
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.linalg import lstsq
from scipy.optimize import minimize
try:
    import pyproj
except ImportError:
    # Directory opzionale dell'ambiente di produzione; non necessaria in R.
    project_runtime=Path(__file__).resolve().parents[4]/'runtime/python_extra'
    sys.path.insert(0,str(project_runtime))
    import pyproj
ROOT=Path(__file__).resolve().parents[1]
d=pd.read_csv(ROOT/'Dati/spazio_v3.csv')
u=pd.read_csv(ROOT/'Dati/casuali_comuni_v3.csv')['u'].to_numpy()
summary=json.loads((ROOT/'Calcoli/summary.json').read_text())
xy=d[['x_m','y_m']].to_numpy();z=d.concentrazione.to_numpy();v=z-z.mean();n=len(z)
D=cdist(xy,xy);A=((D>0)&(D<=260)).astype(float);W=A/A.sum(1)[:,None]
rows=[]
def check(name,value,detail=''):
    value=bool(value);rows.append({'controllo':name,'superato':value,'dettaglio':detail})
    assert value,(name,detail)
def close(x,y,tol=1e-10):return bool(np.max(np.abs(np.asarray(x)-np.asarray(y)))<tol)
def read(name):return pd.read_csv(ROOT/f'Calcoli/{name}.csv')
# Graph construction via independent distances; edge-wise rather than matrix formula for I_A.
edges=list(zip(*np.where(np.triu(A,1))))
IA=n/A.sum()*sum(2*v[i]*v[j] for i,j in edges)/sum(v*v)
IW=sum(v[i]*np.mean(v[np.flatnonzero(A[i])]) for i in range(n))/sum(v*v)
check('Reticolo_e_grafo',n==64 and len(edges)==112 and A.sum()==224 and sorted(set(A.sum(1)))==[2,3,4])
check('Moran_A_W',close([IA,IW],[summary['Moran']['I_A'],summary['Moran']['I_W']]))
coef=np.polyfit(v,W@v,1)
check('Pendenza_e_intercetta_scatter',close(coef,[IW,summary['Moran']['scatter_intercept']]))
null=[]
for b in range(100):
    vb=v[np.argsort(u[b*64:(b+1)*64])]
    null.append(n/A.sum()*sum(2*vb[i]*vb[j] for i,j in edges)/sum(vb*vb))
check('100permutazioni_originali',close(null,read('permutazioni_100_originali').I_A))
check('p_plus1',close((1+sum(np.asarray(null)>=IA))/101,summary['Moran']['p100']) and summary['Moran']['p999']==.001)
# Pairs explicitly enumerated by itertools, independent of R's upper-tri indexing.
pairs=np.array([(D[i,j],(z[i]-z[j])**2/2) for i,j in itertools.combinations(range(n),2)])
means=[];counts=[]
for lo,hi in zip([0,300,600,1000],[300,600,1000,2500]):
    q=pairs[(pairs[:,0]>lo)&(pairs[:,0]<=hi)]
    counts.append(len(q));means.append(q.mean(0))
vg=read('semivariogramma')
check('Variogramma_2016coppie',len(pairs)==2016 and counts==[112,362,476,1066] and close(means,vg[['h','gamma']]))
# Trend: a separate least-squares implementation.
X=np.column_stack([np.ones(n),xy]);beta,_,_,_=lstsq(X,z);res=z-X@beta
check('Trend_e_residui',close(beta,read('trend_coefficienti').stima) and close(res,read('trend_residui').residuo))
check('Road_e_medie',sum(d.y_m<=250)==16 and close(z[d.y_m<=250].mean(),summary['copertura']['media_strada']))
membership=np.column_stack([d.x_m<=1250,d.x_m>=750])
check('Join88con24duplicati',membership.sum()==88 and sum(membership.sum(1)==2)==24 and len(read('join_appartenenze'))==88)
# IDW predictions use SciPy distances and a matrix multiplication; train/test never pooled.
tr=(d.x_m<1250).to_numpy();te=~tr;dt=cdist(xy[te],xy[tr]);weights=dt**-2;weights/=weights.sum(1)[:,None]
pred=weights@z[tr];pred_table=read('previsioni_test')
check('IDW_holdout40_24',sum(tr)==40 and sum(te)==24 and close(pred,pred_table.IDW_p2))
nearest=z[tr][dt.argmin(1)];meanpred=np.repeat(z[tr].mean(),sum(te))
check('Baseline_stesso_test',close(nearest,pred_table.Nearest_neighbour) and close(meanpred,pred_table.Media_train))
allmet=[]
for pp in [meanpred,nearest,pred]:
    e=z[te]-pp;allmet.append([np.mean(abs(e)),np.sqrt(np.mean(e*e)),e.mean()])
check('MAE_RMSE_bias',close(allmet,read('metriche_test')[['MAE','RMSE','bias']]))
inner=read('validazione_interna_IDW')
check('Tuning_esclusivamente_train',set(inner.id).isdisjoint(set(d.loc[te,'id'])) and sorted(inner.frontiera.unique())==[500,750,1000] and list(inner.groupby('p').size())==[24,24,24])
tun=[]
for p in [1,2,3]:
    ee=[]
    for frontier in [500,750,1000]:
        it=(d.x_m<frontier).to_numpy();iv=(d.x_m==frontier).to_numpy()
        ww=cdist(xy[iv],xy[it])**(-p);ww/=ww.sum(1)[:,None]
        ee.extend(z[iv]-ww@z[it])
    tun.append(np.sqrt(np.mean(np.square(ee))))
check('Tuning_RMSE',close(tun,read('tuning_blocchi').RMSE))
# Same kriging objective, solved by constrained optimisation instead of augmented linear system.
okxy=np.array([[0.,0.],[500.,0.],[1000.,0.]])
CC=4*np.exp(-(cdist(okxy,okxy)/800)**2)
c0=4*np.exp(-(cdist([[250.,0.]],okxy)[0]/800)**2)
def obj(w):return float(4-2*w@c0+w@CC@w)
def jac(w):return 2*CC@w-2*c0
optim=minimize(obj,np.ones(3)/3,jac=jac,constraints={'type':'eq','fun':lambda w:w.sum()-1,'jac':lambda w:np.ones(3)},method='SLSQP',options={'ftol':1e-13,'maxiter':100})
check('Kriging_ottimizzazione_indipendente',optim.success and close(optim.x,summary['kriging']['lambda'],1e-6) and close(optim.fun,summary['kriging']['varianza'],1e-10))
check('Kriging_PD_e_peso_negativo',min(np.linalg.eigvalsh(CC))>0 and min(optim.x)<0 and close(sum(optim.x),1))
# Independent native PROJ through pyproj, separate from the WASM sf/GDAL build.
fwd=pyproj.Transformer.from_crs('OGC:CRS84','EPSG:32632',always_xy=True)
px,py=fwd.transform(d.lon.to_numpy(),d.lat.to_numpy());cr=read('coordinate_verificate')
proj_error=float(np.max(np.abs(np.column_stack([px,py])-cr[['UTM_E','UTM_N']].to_numpy())))
check('CRS_sf_contro_pyproj',proj_error<1e-6,f'massimo scarto {proj_error:.12g}m; PROJ Python {pyproj.proj_version_str}')
geo=json.loads((ROOT/'Risultati/campioni_RFC7946.geojson').read_text())
features={f['properties']['id']:f for f in geo['features']}
geoerr=max(np.max(np.abs(np.array(features[row.id]['geometry']['coordinates'])-np.array([row.lon,row.lat]))) for row in d.itertuples())
check('GeoJSON_RFC7946_roundtrip',geo['type']=='FeatureCollection' and 'crs' not in geo and len(features)==64 and geoerr<1e-7 and all(abs(features[row.id]['properties']['concentrazione']-row.concentrazione)<1e-12 for row in d.itertuples()),f'massimo errore {geoerr:.12g}gradi')
check('Esempio_costruito18_15',np.average([10,20],weights=[2,8])==18 and np.mean([10,20])==15 and list(read('esempio_pesi_2_8').n)==[2,8])
expected={'spazio_v3.csv':'1c761968b6a8838ec41510425a5eef7f00f3a99f2627033d1bdefffb679a6331','casuali_comuni_v3.csv':'95b4872007c33a0a2334936536bf0c49eec69f951f4f900f987fda89687879f4'}
check('Dati_originali_sha256',all(hashlib.sha256((ROOT/'Dati'/name).read_bytes()).hexdigest()==sha for name,sha in expected.items()))
result={'controlli':rows,'numero':len(rows),'tutti_superati':all(r['superato'] for r in rows),'pyproj':pyproj.__version__,'PROJ_pyproj':pyproj.proj_version_str,'scarto_proiezione_m':proj_error}
(ROOT/'Verifiche/controlli_indipendenti.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(f'{len(rows)}/{len(rows)} controlli indipendenti superati; sf vs pyproj massimo scarto {proj_error:.6g}m.')
