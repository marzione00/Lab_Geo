from pathlib import Path
import csv,json,sys
import numpy as np
import rasterio
from rasterio.transform import Affine

BASE=Path(__file__).resolve().parent.parent
checks=[]
def check(name,value,detail=None):
    ok=bool(value)
    checks.append({'controllo':name,'esito':'OK' if ok else 'ERRORE','dettaglio':detail})
    assert ok,name

rows=list(csv.DictReader((BASE/'Dati/raster_v3.csv').open()))
rows.sort(key=lambda x:(int(x['riga']),int(x['colonna'])))
Z=np.array([float(r['quota_m']) for r in rows]).reshape(24,30)
with rasterio.open(BASE/'Dati/raster_v3.tif') as src:
    check('Originale: dimensioni e tipo',src.shape==(24,30) and src.dtypes==('float64',))
    check('Originale: EPSG e affine',src.crs.to_epsg()==32632 and src.transform==Affine(30,0,500000,0,-30,5000000))
    check('Originale: CSV corrisponde dopo ribaltamento',np.max(np.abs(src.read(1)[::-1]-Z))<1e-10,
          float(np.max(np.abs(src.read(1)[::-1]-Z))))

gx=(Z[1:-1,2:]-Z[1:-1,:-2])/60
gy=(Z[2:,1:-1]-Z[:-2,1:-1])/60
expected=np.arctan(np.sqrt(gx*gx+gy*gy))*180/np.pi
full=np.full((24,30),np.nan);full[1:-1,1:-1]=expected
saved=list(csv.DictReader((BASE/'Risultati/M12_N20/pendenze.csv').open()))
check('CSV: 616 celle e ordine locale',len(saved)==616 and
      all(float(r['x_m'])==30*((k%28)+1) and float(r['y_m'])==30*((k//28)+1) for k,r in enumerate(saved)))
csv_values=np.array([float(r['pendenza_gradi']) for r in saved]).reshape(22,28)
check('CSV: derivate NumPy indipendenti',np.max(np.abs(csv_values-expected))<1e-10,
      float(np.max(np.abs(csv_values-expected))))

details=[]
for name,target,transform,n_na in [
    ('pendenze_interne.tif',expected,Affine(30,0,500030,0,-30,4999970),0),
    ('pendenze_con_bordo_NoData.tif',full,Affine(30,0,500000,0,-30,5000000),104)]:
    p=BASE/'Risultati/M12_N20'/name
    with rasterio.open(p) as src:
        value=src.read(1,masked=True)
        got=value.filled(np.nan)[::-1]
        mask=np.ma.getmaskarray(value)[::-1]
        check(name+': dimensioni',src.shape==target.shape)
        check(name+': tipo FLOAT64',src.dtypes==('float64',))
        check(name+': CRS EPSG32632 fittizio',src.crs.to_epsg()==32632)
        check(name+': risoluzione30m',src.res==(30,30))
        check(name+': affine e orientamento',src.transform==transform)
        check(name+': tag NoData effettivo',src.nodata==-9999)
        check(name+': maschera e conteggio',np.array_equal(mask,np.isnan(target)) and mask.sum()==n_na,
              {'NoData':int(mask.sum()),'validi':int((~mask).sum())})
        error=float(np.nanmax(np.abs(got-target)))
        check(name+': valori versus NumPy',error<1e-10,error)
        details.append({'file':str(p.relative_to(BASE)),'shape':src.shape,'dtype':src.dtypes[0],
                        'EPSG':src.crs.to_epsg(),'transform':list(src.transform)[:6],
                        'nodata':src.nodata,'AREA_OR_POINT':src.tags().get('AREA_OR_POINT'),
                        'errore_max_gradi':error})
out={'metodo':'Lettura indipendente con rasterio e derivate NumPy dal CSV originale.',
     'rasterio':rasterio.__version__,'GDAL':rasterio.__gdal_version__,'numpy':np.__version__,
     'controlli':checks,'GeoTIFF':details,'esito':'OK'}
(BASE/'Verifiche/audit_geotiff_indipendente.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(len(checks),'controlli indipendenti GeoTIFF/CSV: OK')
