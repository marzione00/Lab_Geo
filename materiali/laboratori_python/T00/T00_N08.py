# Audit del campione importato
# Commento didattico: Verifichiamo numero di righe, unicità degli identificativi e validità dei volumi. Sono contratti del caso didattico, non leggi universali.
from pathlib import Path
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
root=next((p for p in [Path.cwd().resolve(),*Path.cwd().resolve().parents] if (p/'.geologia-v3').exists()),None)
if root is None:raise FileNotFoundError('Aprire Corso_Geologia_Unico')
os.chdir(root)
out=root/'risultati'/'Python'/'T00_N08';out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'dati/campioni_modulo1.csv')
d['densita_g_cm3']=d.massa_g/d.volume_cm3
medie=d.groupby('affioramento',as_index=False)['densita_g_cm3'].mean()
print('Output:',out)

import numpy as np
assert len(d) == 24
assert d["id"].is_unique
assert np.isfinite(d["volume_cm3"]).all()
assert (d["volume_cm3"] > 0).all()
