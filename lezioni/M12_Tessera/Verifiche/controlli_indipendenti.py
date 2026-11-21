"""Verifica indipendente Python/NumPy/rasterio degli output reali R/terra.
Eseguire dalla radice del modulo o con il percorso completo dello script.
Non rigenera né corregge i risultati R.
"""
from pathlib import Path
import csv,json,math,sys
ROOT=Path(__file__).resolve().parents[1]
try: import rasterio
except ImportError:
    sys.path.insert(0,str(ROOT.parents[2]/'runtime/python_extra'))
    import rasterio
import numpy as np
from rasterio.windows import Window
from rasterio.warp import reproject,Resampling
checks=[]
def check(name,ok,detail=None):
    checks.append({'controllo':name,'ok':bool(ok),'dettaglio':detail})
    if not ok: raise AssertionError(name)
def csvdict(p):
    with p.open(newline='') as f:return list(csv.DictReader(f))
def numeric(name,column):
    return np.array([float(r[column]) if r[column] else np.nan for r in csvdict(ROOT/'Calcoli'/f'{name}.csv')])
def grad(M,h=30):
    gy,gx=np.gradient(M,h,h,edge_order=2)
    return gx[1:-1,1:-1],gy[1:-1,1:-1]
def slope(M,h=30):
    gx,gy=grad(M,h);return np.degrees(np.arctan(np.hypot(gx,gy)))
d=csvdict(ROOT/'Dati/raster_v3.csv');Z=np.array([float(r['quota_m']) for r in d]).reshape(24,30)
x=np.arange(30)*30;y=np.arange(24)*30
with rasterio.open(ROOT/'Dati/raster_v3.tif') as src:
    M=src.read(1);profile=src.profile;tr=src.transform
    check('Originale: geometria CRS e NoData',src.shape==(24,30) and src.crs.to_epsg()==32632 and src.nodata==-9999 and tuple(src.res)==(30.,30.))
    check('Originale: orientamento opposto CSV',np.max(np.abs(M-Z[::-1,:]))<1e-10,float(np.max(np.abs(M-Z[::-1,:]))))
    check('Originale: affine corner e pixel area',tuple(tr)[:6]==(30,0,500000,0,-30,5000000))
    rr,cc=np.indices((24,30));ex,ny=src.xy(rr.ravel(),cc.ravel());ex=np.array(ex).reshape(24,30);ny=np.array(ny).reshape(24,30)
    expx=np.broadcast_to(x[None,:]+500015,(24,30));expy=np.broadcast_to((y[::-1]+4999295)[:,None],(24,30))
    check('Centri e traslazione fittizia',np.allclose(ex,expx,atol=1e-10,rtol=0) and np.allclose(ny,expy,atol=1e-10,rtol=0))
    win=src.read(1,window=Window(9,4,8,6))
    check('Lettura finestra rasterio-R',np.max(np.abs(win.ravel()-numeric('finestra48','quota_m')))<1e-10)
    # Secondo binding GDAL con geometria esplicita: controllo del ricampionamento reale.
    dest=np.full((48,60),np.nan,dtype=np.float64)
    dt=rasterio.Affine(15,0,500000,0,-15,5000000)
    reproject(M,dest,src_transform=tr,src_crs=src.crs,dst_transform=dt,dst_crs=src.crs,resampling=Resampling.bilinear)
    r_bi=numeric('ricampionamento_15m','bilineare').reshape(48,60)[::-1]
    # terra/GDAL warp usa interni float32 nel ricampionamento; tolleranza0.2mm esplicita.
    err=float(np.max(np.abs(dest-r_bi)))
    check('Ricampionamento bilineare rasterio-terra',err<2e-4,{'errore_m':err,'tolleranza_m':2e-4})
check('720 celle: area64.8ha',Z.size*30*30/10000==64.8)
mask=np.zeros_like(Z,dtype=bool);mask[4:8,9:15]=True
zm=np.where(mask,np.nan,Z)
check('Maschera:24 e696',mask.sum()==24 and np.isfinite(zm).sum()==696)
summary=json.loads((ROOT/'Calcoli/summary.json').read_text())
check('Medie dominio e zero',abs(np.nanmean(zm)-summary['domini'][1]['media'])<1e-10 and abs(np.nan_to_num(zm).mean()-summary['domini'][2]['media'])<1e-10)
agg=Z.reshape(12,2,15,2).mean(axis=(1,3))
check('Aggregazione: valori e media',np.max(np.abs(agg.ravel()-numeric('aggregato_2x2','quota_m')))<1e-9 and abs(agg.mean()-Z.mean())<1e-10)
gx,gy=grad(Z);sl=slope(Z);asp=np.degrees(np.arctan2(-gx,-gy))%360
check('Gradiente via numpy.gradient',np.max(np.abs(gx.ravel()-numeric('derivate_interne','gx')))<1e-12 and np.max(np.abs(gy.ravel()-numeric('derivate_interne','gy')))<1e-12)
check('Pendenza e azimut indipendenti',np.max(np.abs(sl.ravel()-numeric('derivate_interne','pendenza_gradi')))<1e-10 and np.max(np.abs(asp.ravel()-numeric('derivate_interne','aspect_gradi')))<1e-10)
# Maschera del centro e dei4vicini: ogni invalidità dilatata a croce.
invalid=mask.copy()
invalid[1:,:]|=mask[:-1,:];invalid[:-1,:]|=mask[1:,:];invalid[:,1:]|=mask[:,:-1];invalid[:,:-1]|=mask[:,1:]
invalid[0,:]=True;invalid[-1,:]=True;invalid[:,0]=True;invalid[:,-1]=True
Rmask=numeric('pendenze_maschera','pendenza_gradi').reshape(24,30)
check('Propagazione NoData centro+4vicini',np.array_equal(np.isnan(Rmask),invalid) and np.isfinite(Rmask).sum()==572)
plane=900+.12*x[None,:]+.08*y[:,None];px,py=grad(plane)
check('Prova analitica piano',np.max(np.abs(px-.12))<1e-12 and np.max(np.abs(py-.08))<1e-12 and abs(np.degrees(np.arctan(math.hypot(.12,.08)))-summary['piano']['gradi'])<1e-12)
for az in (315,135):
    a=math.radians(az);e=math.pi/4
    normals=np.stack((-gx,-gy,np.ones_like(gx)),axis=-1);normals/=np.linalg.norm(normals,axis=-1,keepdims=True)
    light=np.array([math.sin(a)*math.cos(e),math.cos(a)*math.cos(e),math.sin(e)])
    h=np.maximum(0,np.einsum('ijk,k->ij',normals,light));rr=numeric('derivate_interne',f'luce{az}')
    check(f'Hillshade{az}: prodotto vettoriale indipendente',np.max(np.abs(h.ravel()-rr))<1e-12)
# Geometria e maschere effettivamente presenti nei tre file esportati.
full=np.full((24,30),np.nan);full[1:-1,1:-1]=sl
for name,expected,valid,nodata,transform in [
 ('pendenze_interne',sl[::-1],616,0,rasterio.Affine(30,0,500030,0,-30,4999970)),
 ('pendenze_con_bordo_NA',full[::-1],616,104,tr),
 ('quote_maschera',zm[::-1],696,24,tr)]:
    with rasterio.open(ROOT/'Risultati'/f'{name}.tif') as src:
        arr=src.read(1,masked=True);vals=arr.filled(np.nan)
        err=float(np.nanmax(np.abs(vals-expected)))
        check(f'Export {name}: geometria tipo NoData',src.crs.to_epsg()==32632 and src.transform==transform and src.dtypes[0]=='float64' and src.nodata==-9999)
        check(f'Export {name}: valori e maschera',np.array_equal(np.isnan(vals),np.isnan(expected)) and np.isfinite(vals).sum()==valid and np.isnan(vals).sum()==nodata and err<1e-10,err)
# Indici da formule indipendenti, confronto scalatura.
xx=np.array([float(r['x_m']) for r in d]);yy=np.array([float(r['y_m']) for r in d])
red=.2+.05*np.cos(yy/150);nir=.4+.1*np.sin(xx/180);nd=(nir-red)/(nir+red)
check('Bande e indice normalizzato',np.max(np.abs(red-numeric('bande_indice','rosso')))<1e-14 and np.max(np.abs(nd-numeric('bande_indice','indice')))<1e-14)
check('Offset non cancellato',np.max(np.abs(((nir+.2)-(red+.2))/((nir+.2)+(red+.2))-numeric('scala_offset_analitico','indice_su_DN_ERRATO')))<1e-14)
# Stessi12blocchi, ordine dichiarato,300campioni originali; nessun confronto di RNG differenti.
bm=np.array([Z[i*6:(i+1)*6,j*10:(j+1)*10].mean() for i in range(4) for j in range(3)])
u=np.array([float(r['u']) for r in csvdict(ROOT/'Dati/casuali_comuni_v3.csv')]);idx=np.floor(u[:3600].reshape(300,12)*12).astype(int)
boot=bm[idx].mean(axis=1)
check('Bootstrap300: tutte le repliche',np.max(np.abs(boot-numeric('bootstrap300_originale','media')))<1e-8)
q=np.quantile(boot,[.025,.975],method='linear')
check('Bootstrap300: quantili type7',np.max(np.abs(q-np.array([summary['bootstrap'][0]['q025'],summary['bootstrap'][0]['q975']])))<1e-8)
for lag in (1,10):
    dif=Z[:,lag:]-Z[:,:-lag];row=summary['dipendenza'][0 if lag==1 else 1]
    check(f'Dipendenza {lag*30}m',dif.size==row['n_coppie'] and abs(np.abs(dif).mean()-row['media_abs'])<1e-10)
# Sensibilità: formule analitiche e area di intersezione ricalcolate da zero.
for h in (10,30,100):
    ax=np.arange(h/2,900,h);ay=np.arange(h/2,600,h);X,Y=np.meshgrid(ax,ay)
    bump=80*np.exp(-((X-450)**2+(Y-300)**2)/(2*120**2));F=900+.12*X+.08*Y+bump
    fs=slope(F,h);gx_true=.12-(X-450)*bump/120**2;gy_true=.08-(Y-300)*bump/120**2
    exact=np.degrees(np.arctan(np.hypot(gx_true,gy_true)))[1:-1,1:-1]
    ax=ax[1:-1];ay=ay[1:-1]
    wx=np.maximum(0,np.minimum(ax+h/2,800)-np.maximum(ax-h/2,100));wy=np.maximum(0,np.minimum(ay+h/2,500)-np.maximum(ay-h/2,100))
    weights=wy[:,None]*wx[None,:];rmse=math.sqrt(np.sum(weights*(fs-exact)**2)/weights.sum())
    reported=next(r for r in summary['sensibilita_analitica'] if r['passo_m']==h)
    check(f'Analitico {h}m: dominio e RMSE',abs(weights.sum()-280000)<1e-8 and abs(rmse-reported['RMSE_pendenza_gradi'])<1e-11,rmse)
report={'stato':'PASS','controlli':len(checks),'superati':sum(c['ok'] for c in checks),'versioni':{'python':sys.version,'numpy':np.__version__,'rasterio':rasterio.__version__,'GDAL_rasterio':rasterio.__gdal_version__},'dettagli':checks}
(ROOT/'Verifiche/controlli_indipendenti.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f"PASS: {len(checks)}/{len(checks)} verifiche Python/rasterio indipendenti")
