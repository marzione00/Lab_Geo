# Stimare la memoria prima del cloud
# Commento didattico: Una matrice di distanze cresce quadraticamente con il numero di campioni. Stimiamo i byte senza allocare il caso più grande.
from pathlib import Path
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
root=next((p for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents] if (p/'.geologia-v3').exists()),None)
if root is None:raise FileNotFoundError('Aprire Corso_Geologia_Unico')
os.chdir(root)
out=root/'risultati'/'Python'/'T00_N19';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'dati/campioni_modulo1.csv')
d['densita_g_cm3']=d.massa_g/d.volume_cm3
medie=d.groupby('affioramento',as_index=False)['densita_g_cm3'].mean()
print('Output:',out)

n=np.array([100,1000,10000],dtype=np.int64)
risultato=pd.DataFrame({'n':n,'MiB_buffer':n*n*8/1024**2})
assert risultato.MiB_buffer.is_monotonic_increasing
display(risultato)