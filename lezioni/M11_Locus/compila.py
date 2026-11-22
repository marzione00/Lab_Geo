#!/usr/bin/env python3
"""Compila due volte il sorgente XeLaTeX, conservando i log di verifica."""
from pathlib import Path
import subprocess, sys
root=Path(__file__).resolve().parent
tex='Locus_M11_statistica_spaziale.tex'
logs=root/'Verifiche';logs.mkdir(exist_ok=True)
for n in (1,2):
    run=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',tex],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (logs/f'xelatex_passaggio_{n}.txt').write_bytes(run.stdout)
    if run.returncode:
        print(run.stdout.decode(errors='replace')[-6000:]);sys.exit(run.returncode)
print('PDF compilato:',root/tex.replace('.tex','.pdf'))
