"""Compilazione portabile della presentazione con XeLaTeX installato."""
from pathlib import Path
import subprocess

module = Path(__file__).resolve().parent
command = ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
           "Polychroma_M08_multivariata.tex"]
for _ in range(2):
    subprocess.run(command, cwd=module, check=True)
