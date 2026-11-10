# Esportare risultati senza sovrascrivere gli input
# Commento didattico: Una tabella in RAM non è ancora una consegna. Salviamo nella cartella del notebook e rileggiamo il file prodotto.
from pathlib import Path
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
root=next((p for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents] if (p/'.geologia-v3').exists()),None)
if root is None:raise FileNotFoundError('Aprire Corso_Geologia_Unico')
os.chdir(root)
out=root/'risultati'/'Python'/'T00_N16';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'dati/campioni_modulo1.csv')
d['densita_g_cm3']=d.massa_g/d.volume_cm3
medie=d.groupby('affioramento',as_index=False)['densita_g_cm3'].mean()
print('Output:',out)

medie.to_csv(out/'medie.csv',index=False)
riletta=pd.read_csv(out/'medie.csv')
np.testing.assert_allclose(riletta.densita_g_cm3,medie.densita_g_cm3)
display(riletta)