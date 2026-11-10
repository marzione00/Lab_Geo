"""Schema editoriale dei contenuti; una pagina conserva un argomento completo."""
from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
class Modulo:
 def __init__(self,codice,titolo,sottotitolo):
  self.codice=codice;self.titolo=titolo;self.sottotitolo=sottotitolo;self.pagine=[];self.sezione='Apertura'
 def sezione_nuova(self,titolo):self.sezione=titolo
 def pagina(self,titolo,testo,destra='',formula='',formula_destra='',figura='',codice='',tikz='',didascalia='',richiamo='',fonti='',origine=''):
  self.pagine.append(dict(sezione=self.sezione,titolo=titolo,testo=testo,destra=destra,formula=formula,formula_destra=formula_destra,figura=figura,codice=codice,tikz=tikz,didascalia=didascalia,richiamo=richiamo,fonti=fonti,origine=origine))
 def salva(self):
  from revisione_R6 import applica
  applica(self)
  (P/'sorgenti/contenuti'/f'{self.codice}.json').write_text(json.dumps(dict(id=self.codice,titolo=self.titolo,sottotitolo=self.sottotitolo,pagine=self.pagine),ensure_ascii=False,indent=2))
  print(self.codice,len(self.pagine),'pagine di contenuto')
 def inserisci_dopo(self,titolo_precedente,**kw):
  i=next(i for i,s in enumerate(self.pagine) if s['titolo']==titolo_precedente)
  old=self.sezione;self.sezione=self.pagine[i]['sezione'];self.pagina(**kw)
  self.pagine.insert(i+1,self.pagine.pop());self.sezione=old

def estratto(mod,id,codice):
 d=P/'estratti'/mod;d.mkdir(exist_ok=True)
 (d/f'{id}.R').write_text(codice.strip()+'\n')
 return f'{mod}/{id}'
