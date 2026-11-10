# Leggere una tabella e riconoscere i tipi
# Commento didattico: L’importazione crea una tabella in memoria. Le prime righe e i tipi permettono di riconoscere conversioni sbagliate prima delle analisi.
from pathlib import Path
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
root=next((p for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents] if (p/'.geologia-v3').exists()),None)
if root is None:raise FileNotFoundError('Aprire Corso_Geologia_Unico')
os.chdir(root)
out=root/'risultati'/'Python'/'T00_N07';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'dati/campioni_modulo1.csv')
d['densita_g_cm3']=d.massa_g/d.volume_cm3
medie=d.groupby('affioramento',as_index=False)['densita_g_cm3'].mean()
print('Output:',out)

import pandas as pd
d = pd.read_csv(
    "dati/campioni_modulo1.csv"
)
print(d.head())
print(d.dtypes)
