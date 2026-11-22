"""Grafici della slide 58 da CSV Meteostat archiviato, senza accessi di rete."""
from pathlib import Path
import gzip
import hashlib
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).parent
data_dir = root / "Dati"
out = root / "Risorse/Figure" if (root / "Risorse").is_dir() else root / "Figure"
out.mkdir(exist_ok=True, parents=True)
raw_path = data_dir / "meteostat_16239_2024_originale.csv"
if not raw_path.exists():
    raw_path.write_bytes(gzip.decompress((root / "input/16239_2024.csv.gz").read_bytes()))
d = pd.read_csv(raw_path)
dates = pd.to_datetime(d[["year", "month", "day"]])
small = pd.DataFrame({
    "data": dates.dt.strftime("%Y-%m-%d"), "tmin": d.tmin,
    "tmax": d.tmax, "pioggia": d.prcp, "sole": d.tsun,
    "nubi_ottavi": d.cldc,
})
small.to_csv(data_dir / "meteostat_ciampino_2024.csv", index=False, na_rep="NA")

plt.rcParams.update({"font.family": "Nimbus Sans", "font.size": 10.5,
                     "axes.labelsize": 11, "axes.titlesize": 14,
                     "pdf.fonttype": 42, "ps.fonttype": 42})
results = {}
for col, title, ylabel, color, name in [
    ("tmax", "Insolazione e Tmax", "Temperatura massima (°C)", "#1D7890", "cor_pos_2024"),
    ("cldc", "Insolazione e nuvolosità", "Copertura nuvolosa (ottavi)", "#C57E42", "cor_neg_2024"),
]:
    ok = d[["tsun", col]].notna().all(axis=1)
    x = d.loc[ok, "tsun"].to_numpy()
    y = d.loc[ok, col].to_numpy()
    b, a = np.polyfit(x, y, 1)
    r = np.corrcoef(x, y)[0, 1]
    fig, ax = plt.subplots(figsize=(5, 3.7))
    fig.patch.set_facecolor("#F8F6F1")
    ax.set_facecolor("#F8F6F1")
    ax.set_axisbelow(True)
    ax.grid(color="#D6DAD9", lw=.5)
    ax.scatter(x, y, s=23, color=color, alpha=.75, linewidths=0)
    xs = np.array([x.min(), x.max()])
    ax.plot(xs, a+b*xs, color=color, lw=1.4)
    ax.set(xlabel="Sole (minuti/giorno)", ylabel=ylabel)
    ax.set_title(title, loc="left", fontweight="bold", pad=24, color="#15283E")
    ax.text(0, 1.025, "Roma/Ciampino · 31 ott.–31 dic. 2024", transform=ax.transAxes,
            fontsize=9.5, color="#657180")
    label=f"n = {len(x)}\nr = {r:.2f}".replace(".", ",")
    ax.text(.96, .95, label, transform=ax.transAxes, va="top", ha="right",
            color="#15283E", fontsize=11, fontweight="bold",
            bbox=dict(facecolor="#F8F6F1", edgecolor="none", alpha=.88, pad=3))
    if col == "cldc":
        ax.set_ylim(-.3, 8.6)
        ax.set_yticks([0, 2, 4, 6, 8])
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["bottom", "left"]:
        ax.spines[side].set_color("#657180")
    ax.tick_params(colors="#253344")
    fig.text(.15, .015, "Meteostat e fornitori · inclusi dati di modello", fontsize=8.2, color="#657180")
    fig.subplots_adjust(left=.15, right=.96, bottom=.19, top=.77)
    fig.savefig(out / f"{name}.pdf")
    fig.savefig(out / f"{name}.png", dpi=130)
    plt.close(fig)
    results[name] = {"n": len(x), "r": float(r), "intercept": float(a), "slope": float(b),
                     "date_min": str(dates[ok].min().date()),
                     "date_max": str(dates[ok].max().date())}

results["raw_csv_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
(root / "correlazioni_verifica.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
