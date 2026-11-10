# Collaudo dei laboratori interattivi · versione 3.0

> Rapporto storico. Il collaudo browser originario confrontava soltanto le coppie di valori numerici finiti e non verificava integralmente nomi, cardinalità e tipi delle metriche. Il consolidamento 3.1.1 corregge questo limite; le prove aggiornate sono riportate in [CONSOLIDAMENTO_3_1_1.md](CONSOLIDAMENTO_3_1_1.md).

## Copertura e calcolo

- 139 attività nei 17 moduli; 147 sezioni inventariate, delle quali 134 con dimostrazioni dedicate e 13 introduttive o di riepilogo raccordate al percorso.
- 594 configurazioni eseguite in R 4.5.0 con ggplot2 3.5.1: configurazione iniziale, estremi dei controlli numerici e opzioni discrete. Nessun errore. Esito dettagliato: `qa/experiments-r.json`.
- 23 famiglie di verifiche analitiche o Monte Carlo: periodi di ritorno, limite GEV, varianza, covarianza, raster, IDW, kriging, PCA, ricampionamento, cronologie, classificazione e riproducibilità. Esito: `qa/experiments-invariants.json`.
- 139 attività eseguite effettivamente in Chromium attraverso webR/R 4.6.0 e ggplot2 4.0.3. Tutte hanno prodotto figure SVG, metriche e CSV; nessun errore, nessuna differenza fra metriche numeriche oltre la tolleranza dichiarata nel collaudo (2,5% relativo con pavimento assoluto 1e-5). Esito: `qa/experiments-webr.json`.

Il confronto browser–R riguarda le configurazioni iniziali. Le condizioni estreme sono state verificate nel runtime R nativo; non sono state tutte ripetute nel browser. Le verifiche controllano coerenza e proprietà note dei modelli didattici e non costituiscono una validazione esterna su dati osservati.

## Formalismo e struttura

La prova DOM virtuale verifica 28 pagine di modulo/progetto, navigazione e 540 espressioni matematiche dei nuovi laboratori, oltre alle 1190 espressioni originali. Sono stati corretti caratteri di controllo che interferivano con alcune definizioni dei simboli. Il controllo automatico impedisce la loro reintroduzione.

Le prove Node verificano copertura, parametri, rotte, collegamenti delle spedizioni e pacchetti locali. Le impronte dei materiali R6 confermano che i file originari sono conservati byte per byte. La build controlla la presenza di tutte le anteprime scientifiche.

## Prove dell’interfaccia

Il laboratorio M05 sugli intervalli di confidenza è stato usato per verificare ricalcolo, confronto A/B, modalità di studio, esecuzione del codice modificato, ripristino e scambio della configurazione JSON. A seme 17, la copertura cambia da 0,935 con correlazione nulla a 0,38 con correlazione comune 0,3. Le figure dei due scenari rimangono disponibili nel confronto.

Lo script R esportato dal browser è stato eseguito separatamente: riproduce copertura 0,38 e errore Monte Carlo 0,0343. Il CSV esportato contiene tutte le 200 repliche e la stessa copertura. L’editor ha eseguito una modifica esplicita del riepilogo e il ripristino ha recuperato il programma originale.

La verifica visuale comprende desktop e viewport di 390 pixel: sul formato stretto i controlli si dispongono in una colonna; i grafici sono scorribili orizzontalmente e mantengono leggibili assi e valori. Le immagini di verifica sono in `qa/preview-laboratorio*.png`. Il pianeta conserva la rotazione durante il laboratorio.

## Ripetizione

Seguire `docs/LABORATORI_INTERATTIVI.md`. La procedura storica di preparazione è stata sostituita dall’unico preparatore corrente `scripts/prepare-browser-harness.mjs`; le istruzioni operative sono nella guida dei laboratori. Le pagine di collaudo sono escluse dalla build finale.

## Ottimizzazione della distribuzione

Sono stati confrontati 1.355 SVG prima e dopo l’ottimizzazione, rasterizzandoli a 850 pixel di larghezza. Tutti conservano le dimensioni; il massimo errore medio assoluto per canale è 0,140 su una scala 0–255. La trasformazione conserva i tracciati assoluti, otto cifre decimali e i valori dei colori; sono escluse le approssimazioni degli archi e delle trasformazioni. I PDF e i caratteri originali rimangono invariati. Il riuso vettoriale dei pannelli TikZ è stato verificato nel browser. Esito: `qa/svg-optimization.json`.
