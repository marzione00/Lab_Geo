# Runtime, pacchetti e installazione
# Commento didattico: Installare un pacchetto e importarlo sono operazioni diverse. Registriamo versioni senza aggiornare l’ambiente durante la lezione.
from pathlib import Path
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
root=next((p for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents] if (p/'.geologia-v3').exists()),None)
if root is None:raise FileNotFoundError('Aprire Corso_Geologia_Unico')
os.chdir(root)
out=root/'risultati'/'Python'/'T00_N14';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'dati/campioni_modulo1.csv')
d['densita_g_cm3']=d.massa_g/d.volume_cm3
medie=d.groupby('affioramento',as_index=False)['densita_g_cm3'].mean()
print('Output:',out)

# Installazione nel terminale:
# python -m pip install pandas
# Uso nel programma:
import pandas as pd
import sys
print(sys.executable)
