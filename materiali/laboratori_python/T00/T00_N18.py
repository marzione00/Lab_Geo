# Una copia in memoria non modifica il CSV
# Commento didattico: Dimostriamo che una modifica alla tabella non modifica il file sorgente, confrontando la sua impronta prima e dopo.
from pathlib import Path
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
root=next((p for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents] if (p/'.geologia-v3').exists()),None)
if root is None:raise FileNotFoundError('Aprire Corso_Geologia_Unico')
os.chdir(root)
out=root/'risultati'/'Python'/'T00_N18';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'dati/campioni_modulo1.csv')
d['densita_g_cm3']=d.massa_g/d.volume_cm3
medie=d.groupby('affioramento',as_index=False)['densita_g_cm3'].mean()
print('Output:',out)

import hashlib
p=root/'dati/campioni_modulo1.csv'
a=hashlib.sha256(p.read_bytes()).hexdigest()
copia=d.copy();copia['nota']='solo RAM'
b=hashlib.sha256(p.read_bytes()).hexdigest()
assert a==b
print('File sorgente immutato:',a==b)