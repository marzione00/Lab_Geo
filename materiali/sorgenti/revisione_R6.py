"""Correzioni della rilettura R6, applicate ai sorgenti prima della compilazione."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent

def applica(modulo):
    for c in json.loads((P/'revisione_R6.json').read_text()):
        if c['modulo'] != modulo.codice: continue
        matches=[s for s in modulo.pagine if s['titolo']==c['titolo']]
        assert len(matches)==1,(modulo.codice,c['titolo'])
        matches[0].update(c['campi'])
    from diagrammi_R6 import genera
    genera(modulo.codice)
