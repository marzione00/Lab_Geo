from autore import Modulo,P
import json,re
m=Modulo('M05','Campionamento, stima e incertezza','Disegni campionari, derivazioni e ricampionamento strutturato')
valori=json.loads((P/'risultati/M05/valori.json').read_text())
def risolvi(s):
 def sostituisci(z):
  v=valori[z[1]]
  return str(int(v)) if z[1] in {'coverage_success','unici_replica','n_progetto'} else f'{v:.3f}'.replace('.',',')
 return re.sub(r'\[\[(\w+)\]\]',sostituisci,s)
for s in json.loads((P/'sorgenti/testi_M05.json').read_text()):
 m.sezione_nuova(s.pop('sezione'))
 m.pagina(**{k:risolvi(v) if isinstance(v,str) else v for k,v in s.items()})
m.salva()
