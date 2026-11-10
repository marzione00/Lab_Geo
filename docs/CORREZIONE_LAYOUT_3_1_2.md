# Correzione del layout 3.1.2

Il test GitHub Actions della versione 3.1.1 si arrestava sulla home mobile:
`document.documentElement.scrollWidth <= innerWidth` risultava falso.
L’errore era reale e non dipendeva dall’installazione di Playwright o dalla configurazione Pages.

## Causa e intervento

I contenitori geometrici dei pianeti sono intenzionalmente più grandi dello schermo,
poiché il motore WebGL usa le loro coordinate per disegnare le sfere nel canvas fisso.
Il contenitore della Terra, collocato oltre il margine destro, contribuiva però anche
alla larghezza scorrevole del documento. Nel browser di verifica la home passava da
340 px di viewport a 710 px di larghezza scorrevole. Lo stesso difetto interessava
le intestazioni dei moduli.

Un contenitore `.planet-viewport`, assoluto e con `overflow: clip`, delimita ora
esclusivamente questi riferimenti decorativi. Testi, titoli e comandi rimangono
esterni al ritaglio. Le dimensioni e le coordinate dei pianeti, il canvas WebGL e
il codice delle rotazioni sono conservati.

## Evidenza raccolta

- Dopo la correzione: home con viewport 340 px e larghezza scorrevole 337 px;
  la differenza dipende dalla barra verticale nel browser con zoom.
- 130 controlli sulle pagine in Chromium, alle larghezze CSS effettive di
  340, 454, 681 e 1363 px: nessun overflow. I dati sono in
  [qa/responsive-3.1.2.json](../qa/responsive-3.1.2.json).
- Tutti i 28 moduli verificati a ogni larghezza; controllate inoltre home,
  mappa, catalogo degli esperimenti, spedizioni, materiali e lettore alle tre
  larghezze maggiori. Verificata separatamente la lettura con formule a 340 px.
- 21 test automatici, controlli HTTP, sicurezza e coerenza superati.
- DOM virtuale: 28 moduli e 1730 espressioni matematiche; controlli SVG e
  importazione del codice superati.

Le larghezze locali sono state ottenute mediante lo zoom del browser. Non si
presentano come una nuova esecuzione del workflow GitHub o come emulazione iOS.
Il calcolo dei 139 esperimenti non è stato modificato né integralmente rieseguito
in questa correzione; il relativo rapporto precedente resta distinto.

## Protezione dalla regressione

`tests/browser.py` conserva il confronto rigoroso della larghezza e verifica home,
28 moduli e lettura con formule a 320, 390, 430, 768 e 1440 px sul runner Chromium.
Prima della misura attende i caratteri del documento. Il nuovo `layout.json`,
incluso nell’artefatto `browser-diagnostics`, registra URL e larghezze; in caso di
errore include anche i rettangoli degli elementi candidati. I candidati richiedono
ispezione: un elemento interno a una regione ritagliata o scorrevole può legittimamente
estendersi oltre il viewport senza causare overflow del documento.

Dopo il caricamento dei file aggiornati nel repository, il workflow deve essere
eseguito nuovamente per verificare il risultato nell’ambiente GitHub.
