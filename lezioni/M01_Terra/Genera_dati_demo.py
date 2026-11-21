"""Genera il CSV didattico della presentazione (nessuna osservazione reale).

Gli studenti eseguono gli esempi R leggendo il CSV gia' fornito: non occorre
Python e non occorre riprodurre una sequenza casuale Python con set.seed().
Generatore: numpy.random.Generator(PCG64), seed = 17012026.
"""
from pathlib import Path
from datetime import date, timedelta
import csv
import math
import numpy as np

out = Path(__file__).parent / "Dati"
out.mkdir(exist_ok=True)
rng = np.random.Generator(np.random.PCG64(17012026))
start, stop = date(2022, 1, 1), date(2024, 12, 31)
dates = [start + timedelta(days=i) for i in range((stop - start).days + 1)]
n = len(dates)
t = np.arange(n, dtype=float)
phase = 2 * np.pi * (t - 110) / 365.25
season = np.sin(phase)

# Variazione meteorologica correlata nel tempo, non rumore indipendente.
innovation = rng.normal(0, 1.7, n)
weather = np.zeros(n)
for i in range(1, n):
    weather[i] = 0.55 * weather[i - 1] + innovation[i]

# Giorni piovosi piu' frequenti nella stagione fresca.
wet = rng.random(n) < (0.28 - 0.10 * season)
rain = np.where(wet, rng.gamma(shape=1.15, scale=5.0, size=n), 0.0)
cloud = np.clip(32 - 8 * season + 42 * wet + rng.normal(0, 17, n), 0, 100)
daylight = 720 + 165 * season
sun = np.clip(daylight * (1 - cloud / 110) + rng.normal(0, 40, n), 0, daylight)
tmin = 10 + 8 * season + 0.15 * t / 365.25 + weather
tmax = tmin + 7 + 3 * (1 - cloud / 100) + rng.normal(0, 1.0, n)

with (out / "meteo_simulati.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["data", "tmin", "tmax", "pioggia", "sole", "nubi"])
    for i, d in enumerate(dates):
        w.writerow([d.isoformat(), f"{tmin[i]:.2f}", f"{tmax[i]:.2f}",
                    f"{rain[i]:.2f}", f"{sun[i]:.1f}", f"{cloud[i]:.1f}"])

print(f"Scritto {out / 'meteo_simulati.csv'}: {n} giorni simulati.")
