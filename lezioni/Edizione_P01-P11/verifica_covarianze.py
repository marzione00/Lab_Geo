"""Confronto indipendente con statsmodels delle covarianze calcolate in R nelle spedizioni P03, P04 e P05.

Uso: python verifica_covarianze.py, dopo aver eseguito R/<id>_figure.R nelle cartelle delle tre lezioni.
Scrive confronto_covarianze.json accanto a questo file.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_hac

LEZIONI = Path(__file__).resolve().parent.parent
results = []
for mod, cartella in (('P03', 'P03_Nilo'), ('P04', 'P04_Geyser'), ('P05', 'P05_CO2')):
    P = LEZIONI / cartella
    if mod == 'P03':
        d = pd.read_csv(P / 'dati/progetti/nile.csv')
        X = sm.add_constant((d.year >= 1898).astype(float))
        y, lag, typ = d.volume_1e8_m3, 3, 'HAC'
    elif mod == 'P04':
        d = pd.read_csv(P / 'dati/progetti/faithful.csv').merge(
            pd.read_csv(P / 'dati/progetti/piani_ricampionamento/faithful_split.csv'), on='row_id').query("set=='train'")
        X = sm.add_constant(d.eruption_min)
        y, typ = d.waiting_min, 'HC3'
    else:
        d = pd.read_csv(P / 'risultati/P05/mensile_modelli.csv')
        X = sm.add_constant(pd.concat([d[['t']], pd.get_dummies(d.month, prefix='mese', drop_first=True, dtype=float)], axis=1))
        y, lag, typ = d.co2_ppm, 12, 'HAC'
    f = sm.OLS(y, X).fit()
    V = cov_hac(f, nlags=lag, use_correction=True) if typ == 'HAC' else f.cov_HC3
    R = pd.read_csv(P / ('risultati/%s/cov_%s.csv' % (mod, typ))).to_numpy()
    err = float(np.max(np.abs(R - np.asarray(V))))
    ok = bool(np.allclose(R, V, rtol=1e-9, atol=1e-10))
    assert ok, (mod, err)
    results.append(dict(progetto=mod, covarianza=typ, errore_massimo=err, esito=ok))
Path(__file__).with_name('confronto_covarianze.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
print(json.dumps(results, indent=2))
