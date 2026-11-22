"""Audit numerico facoltativo e indipendente dal motore R.
Dalla radice del modulo: python Verifiche/controlli_indipendenti.py
Dipendenze opzionali solo per questo audit: numpy e scipy.
Non ristima il SARIMA: ne verifica le metriche, poi ristima OLS/VAR/Granger.
"""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np
from scipy.stats import f as distribuzione_f

ROOT = Path(__file__).resolve().parents[1]
summary = json.loads((ROOT / 'Calcoli/riassunto.json').read_text())

def tabella(name):
    with (ROOT / name).open() as handle:
        return list(csv.DictReader(handle))

def colonna(rows, key):
    return np.array([float(row[key]) for row in rows])

checks = []
def controlla(name, error, tolerance):
    checks.append({'controllo': name, 'scarto_massimo': float(error),
                   'tolleranza': tolerance, 'esito': bool(error <= tolerance)})

forecast = tabella('Calcoli/previsioni_CO2.csv')
errors = colonna(forecast, 'osservato') - colonna(forecast, 'previsto')
for name, actual, expected in [
    ('RMSE', np.sqrt(np.mean(errors**2)), summary['co2']['RMSE_SARIMA']),
    ('MAE', np.mean(abs(errors)), summary['co2']['MAE_SARIMA']),
    ('bias', np.mean(errors), summary['co2']['bias_SARIMA'])]:
    controlla('CO2_' + name + '_numpy', abs(actual - expected), 1e-10)

fossils = tabella('Dati/fossili_simulati.csv')
x = colonna(fossils, 'diametro_tot_um')
y = colonna(fossils, 'diametro_int_um')
test = np.arange(len(fossils)) % 5 == 4
X = np.column_stack([np.ones(len(x)), x])
beta = np.linalg.lstsq(X[~test], y[~test], rcond=None)[0]
expected_beta = np.array([summary['fossili']['intercetta'], summary['fossili']['pendenza']])
controlla('fossili_OLS_numpy', np.max(abs(beta - expected_beta)), 1e-10)
controlla('fossili_RMSE_numpy', abs(np.sqrt(np.mean((y[test] - X[test] @ beta)**2))
                                 - summary['fossili']['RMSE_retta']), 1e-10)

processes = tabella('Dati/processi_simulati.csv')
values = np.column_stack([colonna(processes, 'x_VAR'), colonna(processes, 'y_VAR')])
design = np.column_stack([np.ones(249), values[:249]])
coefficients = np.linalg.lstsq(design, values[1:250], rcond=None)[0]
A = coefficients[1:, :].T
predictions = []
state = values[249].copy()
for _ in range(10):
    state = coefficients[0] + A @ state
    predictions.append(state.copy())
predictions = np.array(predictions)
r_predictions = tabella('Calcoli/previsioni_VAR.csv')
expected_predictions = np.column_stack([colonna(r_predictions, 'X_prevista'),
                                        colonna(r_predictions, 'Y_prevista')])
controlla('VAR_OLS_ricorsione_numpy', np.max(abs(predictions - expected_predictions)), 1e-10)
controlla('VAR_raggio_spettrale_numpy', abs(max(abs(np.linalg.eigvals(A)))
                                         - summary['VAR']['raggio_spettrale']), 1e-10)
for j, direction in [(0, 'Y verso X'), (1, 'X verso Y')]:
    target = values[1:250, j]
    reduced = np.column_stack([np.ones(249), values[:249, j]])
    reduced_beta = np.linalg.lstsq(reduced, target, rcond=None)[0]
    sse_reduced = np.sum((target - reduced @ reduced_beta)**2)
    sse_full = np.sum((target - design @ coefficients[:, j])**2)
    statistic = (sse_reduced - sse_full) / (sse_full / 246)
    p_value = distribuzione_f.sf(statistic, 1, 246)
    expected = next(row for row in tabella('Calcoli/Granger.csv') if row['direzione'] == direction)
    controlla('Granger_F_' + str(j), abs(statistic - float(expected['F'])), 1e-9)
    controlla('Granger_p_' + str(j), abs(p_value - float(expected['p'])), 1e-10)

provenance = json.loads((ROOT / 'Dati/PROVENIENZA.json').read_text())
for dataset in provenance['datasets']:
    digest = hashlib.sha256((ROOT / 'Dati' / dataset['file']).read_bytes()).hexdigest()
    checks.append({'controllo': 'SHA256_' + dataset['file'], 'esito': digest == dataset['sha256']})
assert all(check['esito'] for check in checks), checks
result = {'metodo': 'Ricalcolo indipendente NumPy/SciPy dai CSV, con OLS tramite decomposizione numerica indipendente da lm. Non è una seconda implementazione della stima SARIMA.',
          'controlli': checks, 'tutti_superati': True}
(ROOT / 'Verifiche/controlli_indipendenti_python.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(f"{len(checks)} controlli indipendenti superati.")
