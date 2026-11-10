# Da un algoritmo a una densità
# Commento didattico: Assegnare valori e tradurre una relazione fisica in istruzioni. Massa e volume sono numeri con unità, non semplici simboli da dividere.
from pathlib import Path
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
root=next((p for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents] if (p/'.geologia-v3').exists()),None)
if root is None:raise FileNotFoundError('Aprire Corso_Geologia_Unico')
os.chdir(root)
out=root/'risultati'/'Python'/'T00_N01';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'dati/campioni_modulo1.csv')
d['densita_g_cm3']=d.massa_g/d.volume_cm3
medie=d.groupby('affioramento',as_index=False)['densita_g_cm3'].mean()
print('Output:',out)

massa_g = 107.2
volume_cm3 = 40
rho = massa_g / volume_cm3
print(rho)
assert abs(rho - 2.68) < 1e-10
