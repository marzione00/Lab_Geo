# M11 · Statistica spaziale

Coordinate, associazione e previsione nel territorio.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

9 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M11`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Dato puntuale e supporto areale** · `#laboratorio/m11-supporto` | Confrontare valori locali e medie su superfici crescenti. | [R](../../R/experiments/m11-supporto.R) |
| **Coordinate e metrica delle distanze** · `#laboratorio/m11-coordinate` | Verificare la dipendenza della distanza dalle unità degli assi. | [R](../../R/experiments/m11-coordinate.R) |
| **Aggregazioni territoriali e confini** · `#laboratorio/m11-aggregazione` | Osservare come i confini delle zone modificano una sintesi. | [R](../../R/experiments/m11-aggregazione.R) |
| **Vicinati e matrici dei pesi** · `#laboratorio/m11-vicinati` | Costruire relazioni spaziali a partire da una soglia di distanza. | [R](../../R/experiments/m11-vicinati.R) |
| **Associazione spaziale e permutazioni** · `#laboratorio/m11-moran` | Confrontare Moran I con un riferimento di etichette permutate. | [R](../../R/experiments/m11-moran.R) |
| **Dalle coppie al semivariogramma** · `#laboratorio/m11-variogramma` | Costruire la semivarianza per classi di distanza. | [R](../../R/experiments/m11-variogramma.R) |
| **Copertura geografica del campione** · `#laboratorio/m11-copertura` | Misurare la distanza delle aree dai siti osservati. | [R](../../R/experiments/m11-copertura.R) |
| **Interpolazione e verifica geografica** · `#laboratorio/m11-interpolazione` | Confrontare IDW e un riferimento mediante campioni separati nello spazio. | [R](../../R/experiments/m11-interpolazione.R) |
| **Kriging ordinario e incertezza condizionata** · `#laboratorio/m11-kriging` | Esaminare pesi e previsione di un campo con media costante e covarianza dichiarata. | [R](../../R/experiments/m11-kriging.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**32 slide · 11 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M11_R6.pdf) · [Codice R delle figure](../../materiali/R/M11_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M11_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Dato, posizione e supporto.
- Pagina 6: Coordinate e geometria.
- Pagina 10: Carte, appartenenze e aggregazioni.
- Pagina 13: Vicinati e matrici dei pesi.
- Pagina 16: Associazione spaziale e riferimento inferenziale.
- Pagina 21: Semivarianza e struttura a distanza.
- Pagina 23: Copertura e unità della sintesi.
- Pagina 25: Interpolazione e verifica geografica.
- Pagina 31: Consegna e studio autonomo.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M11_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M11_N01 | Audit delle coordinate e delle unità | [R](../../materiali/laboratori/M11/M11_N01.R) |
| M11_N02 | Latitudine e longitudine invertite | [R](../../materiali/laboratori/M11/M11_N02.R) |
| M11_N03 | Distanza euclidea e invarianti | [R](../../materiali/laboratori/M11/M11_N03.R) |
| M11_N04 | Un arco sulla sfera: haversine | [R](../../materiali/laboratori/M11/M11_N04.R) |
| M11_N05 | Proiezione e controllo di ritorno | [R](../../materiali/laboratori/M11/M11_N05.R) |
| M11_N06 | Rietichettare non significa trasformare | [R](../../materiali/laboratori/M11/M11_N06.R) |
| M11_N07 | Una carta di punti, non una superficie | [R](../../materiali/laboratori/M11/M11_N07.R) |
| M11_N08 | Confini e appartenenza: regole semiaperte | [R](../../materiali/laboratori/M11/M11_N08.R) |
| M11_N09 | Un join spaziale può moltiplicare le righe | [R](../../materiali/laboratori/M11/M11_N09.R) |
| M11_N10 | Buffer e sensibilità alla scala | [R](../../materiali/laboratori/M11/M11_N10.R) |
| M11_N11 | Vicino più prossimo: escludere se stessi | [R](../../materiali/laboratori/M11/M11_N11.R) |
| M11_N12 | Pesi spaziali normalizzati per riga | [R](../../materiali/laboratori/M11/M11_N12.R) |
| M11_N13 | Moran I calcolato esplicitamente | [R](../../materiali/laboratori/M11/M11_N13.R) |
| M11_N14 | Un riferimento di permutazione spaziale | [R](../../materiali/laboratori/M11/M11_N14.R) |
| M11_N15 | Semivarianza e coppie non indipendenti | [R](../../materiali/laboratori/M11/M11_N15.R) |
| M11_N16 | Campionamento di convenienza lungo una strada | [R](../../materiali/laboratori/M11/M11_N16.R) |
| M11_N17 | Medie di blocco e pesi | [R](../../materiali/laboratori/M11/M11_N17.R) |
| M11_N18 | IDW: interpolare con pesi espliciti | [R](../../materiali/laboratori/M11/M11_N18.R) |
| M11_N19 | Validazione spaziale: lasciare fuori Est | [R](../../materiali/laboratori/M11/M11_N19.R) |
| M11_N20 | Consegna GeoJSON e verifica del contenuto | [R](../../materiali/laboratori/M11/M11_N20.R) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
