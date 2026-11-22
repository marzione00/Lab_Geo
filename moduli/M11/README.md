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

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Locus: 110 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M11/Locus_M11_statistica_spaziale.pdf) · [Progetto R della lezione](../../assets/lezioni/M11/Locus_M11_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M11_Locus/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M11`).

- Tappe 17–31: II · Coordinate e distanze.
- Tappe 32–43: III · Carte e appartenenze.
- Tappe 44–55: IV · Vicinati e pesi.
- Tappe 56–70: V · Associazione spaziale.
- Tappe 71–81: VI · Semivarianza.
- Tappe 82–91: VII · Copertura del campione.
- Tappe 92–105: VIII · Previsione spaziale.
- Tappe 106–110: IX · Consegna e studio.

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

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M11.json`, generata dai sorgenti in `lezioni/M11_Locus/`; la spiegazione estesa delle tappe è in `content/lezioni/M11.md`.
