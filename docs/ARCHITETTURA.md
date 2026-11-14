# Architettura e manutenzione

GeoStat Lab è un’applicazione statica nella quale il browser esegue programmi R mediante webR. L’unità principale di navigazione è l’esperimento: i 17 moduli ne organizzano 139, mentre le 11 spedizioni collegano attività preparatorie a casi applicativi. Le 861 slide R6 costituiscono il materiale di approfondimento.

## Sorgenti e prodotti generati

| Sorgente canonica | Prodotti e utilizzo |
|---|---|
| `materiali/` | PDF, sorgenti, dati e programmi originali R6, preservati dalle conversioni dei fine riga |
| `scripts/import-course.py` | Importa R6 in `content/catalogue.json`, `moduli/*/modulo.json` e nelle schede dei moduli; con `--render` ricava gli SVG dai PDF |
| `scripts/labs/build_catalogue.py` | Definisce algoritmi R, parametri, formalismo e raccordo con le sezioni; genera il catalogo degli esperimenti e gli script autonomi |
| `content/prose-*.json` | Spiegazioni, simboli e limiti specifici: ogni attività appartiene a un solo file editoriale |
| `content/research-*.json`, `assets/research/*/provenance.json` | Cinque missioni osservate, codici, campioni congelati e provenienza |
| `content/solution-guides-research.json` | Guide delle missioni e documenti scaricabili prodotti da `scripts/prepare-solution-documents.mjs` |
| `content/course-solutions.json` | Guide P01–P11; `scripts/prepare-course-solutions.R` genera il codice formattato equivalente agli originali |
| `src/solution-terminal.js` | Unica navigazione dei passaggi dei progetti; incorpora il sorgente senza un secondo navigatore |
| `scripts/package-research.mjs` | Programmi autonomi e ZIP delle missioni osservate |
| `R/lab-common.R` | Funzioni statistiche e tema grafico condivisi |
| `scripts/labs/format-code.R` | Formatta il codice R e riallinea `content/experiments.json`, la copia per il collaudo nativo e `R/experiments/` |
| `scripts/public_materials.py` | Prepara i materiali pubblicabili e i manifesti: rapporti e registri editoriali restano nei sorgenti; lo stesso criterio vale per il download didattico |
| `config/site.json` | Autore, sito principale e indirizzi della pubblicazione; i richiami comuni sono compilati dalla build |
| `src/planets.js`, `src/galaxy.js` | Identità dei mondi, schede e navigazione della pagina iniziale |
| `src/galaxy-model.js`, `src/galaxy-scene.js` | Coordinate tridimensionali, particelle, camera prospettica, renderer WebGL e proiezione software |
| `src/experiments.js` | Interfaccia dei laboratori e definizione delle tre fasi di ciascuna spedizione |
| `scripts/update-module-guides.mjs` | Allinea le 28 schede README al catalogo e alle spedizioni effettivamente utilizzati dal sito |
| `scripts/labs/package-downloads.py` | Rigenera entrambi gli archivi scaricabili e la mappa CSV; `--check` ne verifica membri e contenuti |

`package.json` identifica la versione applicativa, ripresa dal catalogo degli esperimenti e dalla consegna ZIP. Il campo `version` di `content/catalogue.json` identifica invece il formato del catalogo R6; il formato JSON delle configurazioni importabili ha una propria versione, verificata da `src/security.js`.

## Flusso dell’applicazione

La build compila i cataloghi in risorse JavaScript locali, copia gli asset pubblicabili e applica CSP e SRI. `src/app.js` gestisce il routing e la consultazione delle slide; `src/experiments.js` gestisce parametri, appunti, confronti ed esportazioni. `src/lab-engine.js` avvia R in un worker, esegue il codice approvato e restituisce tabelle, metriche e SVG. `src/security.js` valida ingressi e risultati prima della visualizzazione.

Le figure precalcolate, identificate nell’interfaccia come configurazione iniziale, consentono la lettura prima che R sia disponibile. Il risultato ricalcolato riporta il proprio ambiente: l’anteprima nativa e il runtime webR possono usare versioni differenti. I dettagli sono nella [guida dei laboratori](LABORATORI_INTERATTIVI.md).

La grafica planetaria dispone di rendering WebGL e di un’alternativa Canvas 2D. MathJax locale compone le formule; le presentazioni SVG conservano i tracciati del template originale. Nessun backend applicativo archivia dati degli studenti: appunti e progresso rimangono nel browser.

## Navigazione

| Rotta | Contenuto |
|---|---|
| `#indice` | Pagina iniziale |
| `#mappa` | Atlante dei pianeti |
| `#sistema-M01?v=18` | Sistema sintetico nella configurazione indicata |
| `#esplorazione/M01-b?v=18` | Missione complementare e confronto dei mondi della stessa configurazione |
| `#taccuino`, `#taccuino-esplorazioni` | Annotazioni del corso e delle esplorazioni, separate |
| `#esperimenti` | Ricerca dei 139 esperimenti |
| `#laboratorio/m05-intervalli` | Esperimento, controlli e risultati R |
| `#modulo-M05` | Percorso sperimentale del modulo |
| `#progetti`, `#modulo-P01` | Indice delle spedizioni e relative fasi |
| `#catalogo`, `#materiali` | Indice testuale e risorse |
| `#modulo-M05/slide/44`, `#modulo-M05/codici` | Approfondimento R6 e programmi originali |

I percorsi degli asset sono relativi alla radice del sito e supportano sottocartelle GitHub Pages. Le rotte a frammento vanno aperte sul sito avviato, non sulla pagina del repository GitHub.

## Aggiornamenti riproducibili

Per correggere le slide, aggiornare e ricollaudare le fonti in `materiali/`, verificare i PDF e soltanto dopo aggiornare il manifesto approvato. `python3 scripts/import-course.py --render` richiede Poppler e riallinea il contenuto web; la compilazione originaria richiede anche l’ambiente R, Python e XeLaTeX del corso.

Per gli esperimenti, modificare il generatore e il file editoriale dell’attività, quindi seguire la [sequenza di rigenerazione](LABORATORI_INTERATTIVI.md#struttura-dei-sorgenti). Quando cambia un algoritmo o un parametro occorre rigenerare e ricollaudare anche le basi numeriche e le figure. Le sole correzioni editoriali devono preservare codice R e parametri approvati.

Dopo una modifica eseguire `npm test` e `npm run test:dom`; per le modifiche al calcolo o al suo collaudo eseguire anche il catalogo nel browser. `npm run test:consistency` controlla copie generate, limiti specifici, schede dei moduli, guide delle soluzioni, programmi scaricabili, membri e byte degli archivi e collegamenti. Il controllo R locale confronta anche gli alberi delle espressioni dei programmi P01–P11 con gli originali. Non rigenerare automaticamente hash o risultati attesi per cancellare una discrepanza non spiegata.

## Collaudo e pubblicazione

Un solo preparatore, `scripts/prepare-browser-harness.mjs`, genera la pagina temporanea di collaudo. `npm run test:browser` lo usa e rimuove i file al termine; per una verifica manuale aprire la pagina direttamente e impostare il viewport tramite gli strumenti del browser. La distribuzione con header completi vieta l’incorporamento. Un’eventuale pagina temporanea isolata per confrontare larghezze CSS non verifica tali header e non sostituisce il collaudo della pagina effettiva; non deve entrare in `dist/` pubblicato.

Il confronto delle metriche è condiviso tra Node e browser: richiede nomi univoci, uguale insieme di metriche, tipi compatibili, uguaglianza dei risultati testuali e una tolleranza esplicita per i numeri. Le differenze fanno fallire l’attività. Il [rapporto della revisione 3.2.2](REVISIONE_3_2_2.md) conserva le relative evidenze storiche; i nuovi interventi sono descritti nel [registro delle modifiche](../CHANGELOG.md).

L’output `dist/` è ricostruibile e non deve contenere le pagine di collaudo nella pubblicazione. Le procedure operative sono mantenute in [DEPLOYMENT.md](../DEPLOYMENT.md); il modello di fiducia e i limiti dell’hosting sono in [SICUREZZA.md](SICUREZZA.md).
