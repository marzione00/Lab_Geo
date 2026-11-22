# P06 · Dai campioni alla validazione spaziale

Vicinato, permutazioni e trasferimento verso un settore escluso.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Valuta una previsione geografica nel settore non utilizzato per costruire il modello e documenta la copertura territoriale.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Definire la geometria

- **Coordinate e metrica delle distanze**: Verificare la dipendenza della distanza dalle unità degli assi. [Programma R](../../R/experiments/m11-coordinate.R); rotta del sito: `#laboratorio/m11-coordinate`.
- **Copertura geografica del campione**: Misurare la distanza delle aree dai siti osservati. [Programma R](../../R/experiments/m11-copertura.R); rotta del sito: `#laboratorio/m11-copertura`.

### Esaminare la struttura

- **Vicinati e matrici dei pesi**: Costruire relazioni spaziali a partire da una soglia di distanza. [Programma R](../../R/experiments/m11-vicinati.R); rotta del sito: `#laboratorio/m11-vicinati`.
- **Dalle coppie al semivariogramma**: Costruire la semivarianza per classi di distanza. [Programma R](../../R/experiments/m11-variogramma.R); rotta del sito: `#laboratorio/m11-variogramma`.

### Verificare altrove

- **Interpolazione e verifica geografica**: Confrontare IDW e un riferimento mediante campioni separati nello spazio. [Programma R](../../R/experiments/m11-interpolazione.R); rotta del sito: `#laboratorio/m11-interpolazione`.
- **Kriging ordinario e incertezza condizionata**: Esaminare pesi e previsione di un campo con media costante e covarianza dichiarata. [Programma R](../../R/experiments/m11-kriging.R); rotta del sito: `#laboratorio/m11-kriging`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P06: 27 tappe.**

[Presentazione PDF](../../assets/lezioni/P06/P06_Validazione.pdf) · [Progetto R della spedizione](../../assets/lezioni/P06/Spedizione_P06_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P06_Validazione/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P06`).

- Tappa 3: Il caso guida.
- Tappe 4–7: Geometria e osservazioni sintetiche.
- Tappe 8–11: Vicinato e riferimento di permutazione.
- Tappe 12–18: Previsione e verifica nel settore orientale.
- Tappe 19–25: Laboratori della spedizione.
- Tappa 26: Sintesi.
- Tappa 27: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P06_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P06.json`, generata dai sorgenti in `lezioni/P06_Validazione/`.
