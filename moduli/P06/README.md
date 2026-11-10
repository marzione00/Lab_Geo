# P06 · Dai campioni alla validazione spaziale

Vicinato, permutazioni e trasferimento verso un settore escluso.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Valuta una previsione geografica nel settore non utilizzato per costruire il modello e documenta la copertura territoriale.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Definire la geometria

- **Coordinate e metrica delle distanze** — Verificare la dipendenza della distanza dalle unità degli assi. [Programma R](../../R/experiments/m11-coordinate.R); rotta del sito: `#laboratorio/m11-coordinate`.
- **Copertura geografica del campione** — Misurare la distanza delle aree dai siti osservati. [Programma R](../../R/experiments/m11-copertura.R); rotta del sito: `#laboratorio/m11-copertura`.

### Esaminare la struttura

- **Vicinati e matrici dei pesi** — Costruire relazioni spaziali a partire da una soglia di distanza. [Programma R](../../R/experiments/m11-vicinati.R); rotta del sito: `#laboratorio/m11-vicinati`.
- **Dalle coppie al semivariogramma** — Costruire la semivarianza per classi di distanza. [Programma R](../../R/experiments/m11-variogramma.R); rotta del sito: `#laboratorio/m11-variogramma`.

### Verificare altrove

- **Interpolazione e verifica geografica** — Confrontare IDW e un riferimento mediante campioni separati nello spazio. [Programma R](../../R/experiments/m11-interpolazione.R); rotta del sito: `#laboratorio/m11-interpolazione`.
- **Kriging ordinario e incertezza condizionata** — Esaminare pesi e previsione di un campo con media costante e covarianza dichiarata. [Programma R](../../R/experiments/m11-kriging.R); rotta del sito: `#laboratorio/m11-kriging`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**17 slide · 7 figure · 4 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P06_R6.pdf) · [Codice R delle figure](../../materiali/R/P06_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P06_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Geometria e osservazioni sintetiche.
- Pagina 7: Vicinato e riferimento di permutazione.
- Pagina 11: Previsione e verifica nel settore orientale.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P06_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
