# Atlante planetario di GeoStat Lab

Il sito conserva integralmente i materiali didattici R6 e aggiunge una navigazione fra 17 mondi, ciascuno associato a un modulo, e 11 spedizioni applicative. La home mantiene la Terra rotante. La carta stellare permette di scegliere ogni destinazione e di filtrare cinque regioni tematiche.

## Navigazione

- `#indice`: pagina iniziale e ripresa dell'ultima lezione.
- `#mappa`: 17 pianeti e cinque regioni tematiche.
- `#catalogo`: indice testuale, ricerca e filtri.
- `#progetti`: 11 spedizioni con collegamenti ai moduli pertinenti.
- `#modulo-M14`: esempio di pagina di un modulo.
- `#modulo-M14/slide/3`: slide originale, testo con formule e codice.
- `#modulo-M14/codici`: script delle figure e laboratori scaricabili.
- `#materiali`: documentazione, dati e archivio di lavoro.

Il trasferimento fra mondi dura 1,45 secondi e può essere saltato con il pulsante dedicato o con Esc. La rotazione prosegue nella mappa, nelle pagine dei moduli, nelle slide, nel testo e nei laboratori. Il comando Pausa rotazione è manuale. La preferenza di sistema per il movimento ridotto elimina i trasferimenti animati; resta disponibile il comando esplicito di pausa. La pagina sospende il lavoro grafico quando la scheda non è visibile.

## Rendering e personalizzazione

`src/planets.js` contiene identità, palette, inclinazione, fase, velocità e relazioni delle spedizioni. `src/planet.frag` descrive il rendering WebGL: rotazione della superficie, illuminazione fissa, atmosfera, emissione vulcanica, fasce gassose e anelli con occlusione e ombre. `src/space.js` gestisce l'unica superficie grafica, la navigazione e la continuità temporale.

Se il browser non dispone di WebGL, `src/space-cpu.js` proietta le texture su una sfera in Canvas 2D e aggiorna le longitudini nel tempo. La luce e il bordo del pianeta rimangono fissi anche in questo caso. Questa modalità usa una risoluzione inferiore, mantenendo leggibile l'interfaccia e attiva la rotazione. Alcuni dettagli di illuminazione differiscono dal rendering WebGL.

Le texture procedurali già incluse si possono rigenerare con `python3 scripts/bake-planets.py` in un ambiente Python con moderngl, numpy, Pillow e un contesto EGL. Queste dipendenze servono soltanto alla rigenerazione e al collaudo degli shader; la build ordinaria del sito richiede solo Node.

`src/space.css` definisce la scenografia. Le slide SVG, i PDF, i font didattici e i sorgenti del corso non vengono modificati. I pianeti sono illustrativi e la velocità è scelta per rendere osservabile il movimento.

## Materiali e stato locale

L'archivio `assets/downloads/GeoStatLab_codice_dati_R6.zip` conserva la cartella `materiali/` con R, Python, dati, sorgenti, TikZ e documentazione per il lavoro locale. Le figure e i resoconti generati rimangono disponibili separatamente nel sito completo. Le pagine studiate e l'ultima lezione vengono salvate nel browser solo tramite le funzionalità previste; aprire un pianeta non segna un modulo come completato.

## Verifiche

`npm test` controlla copertura del corso, conservazione dei materiali tramite SHA-256, corrispondenza dei laboratori, rotte, ricerca, stato locale, associazioni planetarie e risorse della distribuzione.

`npm run test:dom` verifica tutti i 28 fascicoli, la mappa e i filtri, pausa e ripresa, navigazione e 1.190 espressioni matematiche con MathJax. Richiede jsdom 26.1.0.

`python3 scripts/check-planet-rendering.py` compila lo shader in un contesto OpenGL software, confronta due fotogrammi per tutte le 28 destinazioni e verifica che la superficie cambi mantenendo invariata la sagoma. Non sostituisce una verifica WebGL nel browser.

Il collaudo nel browser disponibile ha utilizzato Canvas 2D perché WebGL non era esposto. Sono stati controllati navigazione, viaggio, lettura, formule, pausa e adattamento a schermi stretti. I materiali R6 conservano i risultati delle precedenti verifiche numeriche; questa revisione riguarda l'interfaccia.
