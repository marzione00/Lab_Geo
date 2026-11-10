from pathlib import Path
import json,csv,io,zipfile
root=Path(__file__).resolve().parents[2];out=root/'assets/downloads';out.mkdir(exist_ok=True)
c=json.loads((root/'content/experiments.json').read_text())
s=io.StringIO();w=csv.writer(s,lineterminator="\n");w.writerow(['modulo','sezione','titolo_sezione','funzione','esperimenti'])
for x in c['coverage']:w.writerow([x.get('module'),x.get('section'),x.get('title',x.get('sectionTitle','')),x['role'],';'.join(x['activities'])])
(out/'GeoStatLab_mappa_esperimenti.csv').write_text(s.getvalue(),encoding='utf-8-sig')
with zipfile.ZipFile(out/'GeoStatLab_esperimenti_R.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((root/'R').rglob('*.R')):z.write(p,p.relative_to(root))
 for p in ['content/experiments.json','vendor/r-packages-lock.json','docs/LABORATORI_INTERATTIVI.md','scripts/labs/check-r.R','scripts/labs/check-invariants.R']:z.write(root/p,p)
 z.writestr('LEGGIMI.txt','GeoStat Lab · 139 esperimenti R\n\nOgni file in R/experiments è autonomo e include funzioni e parametri.\nInstallare ggplot2 e jsonlite; svglite serve per esportare figure SVG.\nEseguire con Rscript R/experiments/NOME.R oppure aprire il file in RStudio.\nIl browser usa R 4.6.0 e ggplot2 4.0.3; il collaudo nativo usa R 4.5.0 e ggplot2 3.5.1.\nI dati sono sintetici: generatore, ipotesi e seme sono dichiarati nel codice.\nVedere docs/LABORATORI_INTERATTIVI.md per copertura e limiti.\n')
print('Archivio R e mappa delle sezioni aggiornati')
