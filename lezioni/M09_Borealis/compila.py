"""Compila la presentazione dalla propria cartella con due passaggi XeLaTeX."""
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parent
if shutil.which("xelatex") is None:
    raise SystemExit("XeLaTeX non trovato. Installare una distribuzione TeX completa.")
for _ in range(2):
    subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
         "Borealis_M09_serie_temporali.tex"],
        cwd=root, check=True
    )
print(root / "Borealis_M09_serie_temporali.pdf")

