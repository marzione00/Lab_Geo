# Cloud simulato: recuperare un output effimero
# Commento didattico: Simuliamo localmente un runtime temporaneo e una destinazione persistente. Non stiamo aprendo un vero account cloud.
from pathlib import Path
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
root=next((p for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents] if (p/'.geologia-v3').exists()),None)
if root is None:raise FileNotFoundError('Aprire Corso_Geologia_Unico')
os.chdir(root)
out=root/'risultati'/'Python'/'T00_N20';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'dati/campioni_modulo1.csv')
d['densita_g_cm3']=d.massa_g/d.volume_cm3
medie=d.groupby('affioramento',as_index=False)['densita_g_cm3'].mean()
print('Output:',out)

import tempfile, shutil
with tempfile.TemporaryDirectory() as tmp:
    f=Path(tmp)/'tabella.csv'
    pd.DataFrame({'media':[2.7]}).to_csv(f,index=False)
    shutil.copy2(f,out/'recuperato.csv')
    vecchio=f
assert not vecchio.exists() and (out/'recuperato.csv').exists()
print('Copia recuperata:',out/'recuperato.csv')