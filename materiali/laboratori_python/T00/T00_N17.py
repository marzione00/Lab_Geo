# Identificare il processo di calcolo
# Commento didattico: Osserviamo il processo che esegue il codice e distinguiamo runtime, sistema operativo e cartella corrente.
from pathlib import Path
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
root=next((p for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents] if (p/'.geologia-v3').exists()),None)
if root is None:raise FileNotFoundError('Aprire Corso_Geologia_Unico')
os.chdir(root)
out=root/'risultati'/'Python'/'T00_N17';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'dati/campioni_modulo1.csv')
d['densita_g_cm3']=d.massa_g/d.volume_cm3
medie=d.groupby('affioramento',as_index=False)['densita_g_cm3'].mean()
print('Output:',out)

import sys, platform, os
risultato=pd.DataFrame({'proprieta':['versione','processo','cartella'],'valore':[platform.python_version(),str(os.getpid()),str(Path.cwd())]})
display(risultato)