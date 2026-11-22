# Fonti e convenzioni scientifiche di M11 Locus

Consultazione delle fonti: 20 novembre 2026. I collegamenti seguenti sono documentazione primaria dei progetti o lo standard tecnico originale. I numeri del caso guida provengono dai CSV locali e dall'esecuzione R registrata, non da valori ripresi dalla documentazione.

## Provenienza del materiale didattico

- Repository: [marzione00/Lab_Geo](https://github.com/marzione00/Lab_Geo), commit `649f7cc577b96bd1044d81e78a2f530813e4f96b`.
- Dataset: `materiali/dati/spazio_v3.csv` e `materiali/dati/casuali_comuni_v3.csv`.
- Protocolli: `materiali/laboratori/M11/M11_N01.R` fino a `M11_N20.R`, `materiali/R/M11_figure.R` e i nove esperimenti M11.
- La copia dei dati è verificata con SHA-256 in `Dati/PROVENIENZA.json`; la provenienza dei 36 file dello snapshot è documentata dal confronto con i Git blob in `PROVENIENZA_GIT_SITO.json`.

## Coordinate e scambio dei dati

1. [sf: `st_crs` e `st_set_crs`](https://r-spatial.github.io/sf/reference/st_crs.html). Assegnare o sostituire il CRS modifica il metadato, non ricalcola le coordinate. La documentazione descrive anche la gestione dell'ordine degli assi e la distinzione fra ordine dell'autorità e ordine GIS.
2. [sf: `st_transform`](https://r-spatial.github.io/sf/reference/st_transform.html). La trasformazione usa i riferimenti di origine e destinazione. `OGC:CRS84` esplicita l'ordine longitudine-latitudine; il modulo lo usa per evitare ambiguità nella specificazione degli assi.
3. [PROJ: Universal Transverse Mercator](https://proj.org/en/stable/operations/projections/utm.html). Definizione e parametri della proiezione UTM. L'esempio vicino a 9° E, 45° N viene trasformato in WGS 84 / UTM 32N, EPSG:32632. I metri locali del dataset rimangono una distinta rappresentazione convenzionale.
4. [RFC 7946, The GeoJSON Format, sezioni 3.1.1 e 4](https://www.rfc-editor.org/rfc/rfc7946.html). GeoJSON conforme allo standard usa longitudine e latitudine in gradi decimali, riferite a WGS 84. L'output viene realmente scritto e riletto con `sf`, verificando ID, attributi e coordinate.

La haversine è implementata esplicitamente nel codice, con raggio 6 371 000 m e conversione dei gradi in radianti. È una distanza sferica; non viene qualificata come geodetica ellissoidale. La correttezza del CRS iniziale non può essere dimostrata dal solo ritorno numerico dopo una trasformazione.

## Pesi, Moran e inferenza

5. [spdep: `moran.test`](https://r-spatial.github.io/spdep/reference/moran.test.html). La documentazione distingue le ipotesi del riferimento e richiama la sensibilità al grafo dei vicini. Nel modulo l'indice è calcolato in R base dalla formula dichiarata, usando separatamente A e W.
6. [spdep: `moran.mc`](https://r-spatial.github.io/spdep/reference/moran.mc.html). Il riferimento Monte Carlo riassegna i valori mantenendo fissi i pesi. Il modulo conserva le 100 permutazioni originali e aggiunge un esperimento distinto di 999 permutazioni; la formula plus1 e l'alternativa positiva sono esplicite.
7. [spdep: `lm.morantest`](https://r-spatial.github.io/spdep/reference/lm.morantest.html). L'inferenza sui residui di un modello stimato richiede un trattamento specifico. Il modulo usa il confronto sui residui come descrizione e non attribuisce esattezza alla loro permutazione libera.

L'identità fra pendenza dello scatter e I_W segue dal centramento del vettore in ascissa e da S0(W)=n. Non si attribuisce la medesima pendenza all'indice basato su A. Le classificazioni HH/LL/HL/LH sono descrittive e non mappe di test locali.

## Semivariogramma e previsione

8. [gstat: `variogram`](https://r-spatial.github.io/gstat/reference/variogram.html). La documentazione descrive nuvola delle coppie, variogrammi dei residui, classi irregolari e tolleranze direzionali. I risultati riportano numero di coppie, distanza media e semivarianza. Nel modulo i bin sono implementati esplicitamente e i conteggi non vengono trattati come repliche indipendenti.
9. [gstat: `vgm`](https://r-spatial.github.io/gstat/reference/vgm.html). Specificazione dei modelli, sill parziale e componenti di errore. Nel modulo le curve teoriche sono esempi dichiarati con convenzioni di scala esplicite, non modelli automaticamente adattati al dataset.
10. [gstat: `krige` e `idw`](https://r-spatial.github.io/gstat/reference/krige.html). La documentazione distingue kriging semplice, ordinario e universale, bersagli puntuali e di blocco e pesi IDW. Il modulo risolve il piccolo sistema di kriging in R base e verifica la varianza con due formule equivalenti e con un'ottimizzazione indipendente in Python.

I parametri di covarianza dell'esempio sono noti per costruzione. La varianza riportata esprime l'errore sotto quel modello; non include automaticamente l'incertezza dei parametri o del modello. La superficie IDW sui 64 siti è descrittiva. Il test sui 24 siti orientali usa esclusivamente 40 siti occidentali e p=2 prefissato. Il tuning opzionale su tre frontiere è confinato ai 40 siti di addestramento.

## Esecuzione e verificabilità

- [WebR: progetto R-WASM](https://docs.r-wasm.org/webr/latest/). Esecuzione effettiva di R nell'ambiente WebAssembly.
- [Repository binario ufficiale R-WASM per R 4.6](https://repo.r-wasm.org/bin/emscripten/contrib/4.6/). I pacchetti usati sono registrati, con versioni e SHA-256, in `RUNTIME_E_PACCHETTI.json`.
- Sessione di produzione: R 4.6.0, WebR 0.6.1, sf 1.1-3, GEOS 3.11.2, GDAL 3.8.1, PROJ 9.2.0.
- Risultati verificati: 25 controlli R, 20 controlli indipendenti Python e 40 PDF scientifici vettoriali. I rapporti locali documentano i controlli effettuati e i loro esiti, senza sostituire le ipotesi scientifiche.

Le pagine di documentazione possono mostrare una versione più recente di quella usata per l'esecuzione. Le versioni della sessione, i protocolli e le impronte dei dati nel pacchetto identificano il calcolo effettivamente riprodotto.
