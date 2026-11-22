# M09 · Serie temporali ambientali

Calendario, dipendenza, trasformazioni e stazionarietà.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

7 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M09`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Calendario e osservazioni mancanti** · `#laboratorio/m09-calendario` | Distinguere distanza temporale e posizione nella tabella. | [R](../../R/experiments/m09-calendario.R) |
| **Risoluzione temporale e copertura** · `#laboratorio/m09-aggregazione` | Esaminare gli effetti dell’aggregazione di una serie. | [R](../../R/experiments/m09-aggregazione.R) |
| **Trend, stagionalità e media mobile** · `#laboratorio/m09-smoothing` | Confrontare componenti note e stima mediante smoothing. | [R](../../R/experiments/m09-smoothing.R) |
| **Ritardi e autocorrelazione** · `#laboratorio/m09-autocorrelazione` | Collegare coppie temporali e dipendenza a un ritardo. | [R](../../R/experiments/m09-autocorrelazione.R) |
| **Processo stazionario e passeggiata casuale** · `#laboratorio/m09-stazionarieta` | Confrontare memoria e accumulo delle innovazioni. | [R](../../R/experiments/m09-stazionarieta.R) |
| **Trasformazione e differenziazione** · `#laboratorio/m09-differenze` | Valutare la rimozione di un trend e i suoi effetti sulla dipendenza. | [R](../../R/experiments/m09-differenze.R) |
| **Diagnosi ADF e KPSS mediante simulazione** · `#laboratorio/m09-diagnosi` | Confrontare due statistiche con ipotesi nulle differenti. | [R](../../R/experiments/m09-diagnosi.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Borealis: 106 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M09/Borealis_M09_serie_temporali.pdf) · [Progetto R della lezione](../../assets/lezioni/M09/Borealis_M09_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M09_Borealis/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M09`).

- Tappe 15–25: II · Aggregazione e risoluzione.
- Tappe 26–39: III · Trend, stagione e smoothing.
- Tappe 40–53: IV · Ritardi e autocorrelazione.
- Tappe 54–67: V · Processi e stazionarietà.
- Tappe 68–83: VI · Trend e trasformazioni.
- Tappe 84–96: VII · Diagnosi con ADF e KPSS.
- Tappe 97–106: VIII · Analisi della co₂.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M09_N01 | Dati storici, non una misura aggiornata | [R](../../materiali/laboratori/M09/M09_N01.R) |
| M09_N02 | Aggregare e conservare un indicatore di copertura | [R](../../materiali/laboratori/M09/M09_N02.R) |
| M09_N03 | Confrontare la ricostruzione con il file fornito | [R](../../materiali/laboratori/M09/M09_N03.R) |
| M09_N04 | Un calendario completo prima di creare un oggetto ts | [R](../../materiali/laboratori/M09/M09_N04.R) |
| M09_N05 | Vedere il ciclo entro gli anni | [R](../../materiali/laboratori/M09/M09_N05.R) |
| M09_N06 | Media mobile centrata e causale | [R](../../materiali/laboratori/M09/M09_N06.R) |
| M09_N07 | LOESS e significato dello span | [R](../../materiali/laboratori/M09/M09_N07.R) |
| M09_N08 | Anomalie rispetto a una base esplicita | [R](../../materiali/laboratori/M09/M09_N08.R) |
| M09_N09 | Decomposizione e ricostruzione | [R](../../materiali/laboratori/M09/M09_N09.R) |
| M09_N10 | Tre processi, tre domande | [R](../../materiali/laboratori/M09/M09_N10.R) |
| M09_N11 | La correlazione con il passato | [R](../../materiali/laboratori/M09/M09_N11.R) |
| M09_N12 | ACF di processi diversi | [R](../../materiali/laboratori/M09/M09_N12.R) |
| M09_N13 | Differenziare una volta | [R](../../materiali/laboratori/M09/M09_N13.R) |
| M09_N14 | Differenziare troppo crea struttura | [R](../../materiali/laboratori/M09/M09_N14.R) |
| M09_N15 | Trend deterministico e differenza non sono sinonimi | [R](../../materiali/laboratori/M09/M09_N15.R) |
| M09_N16 | ADF e KPSS: due ipotesi diverse | [R](../../materiali/laboratori/M09/M09_N16.R) |
| M09_N17 | CO2: livello, differenza stagionale e differenza combinata | [R](../../materiali/laboratori/M09/M09_N17.R) |
| M09_N18 | Una diagnosi, non soltanto un p-value | [R](../../materiali/laboratori/M09/M09_N18.R) |
| M09_N19 | Laboratorio applicativo — Numero di osservazioni | [R](../../materiali/laboratori/M09/M09_N19.R) |
| M09_N20 | Laboratorio applicativo — Sovradifferenziazione | [R](../../materiali/laboratori/M09/M09_N20.R) |

## Tracciabilità

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M09.json`, generata dai sorgenti in `lezioni/M09_Borealis/`; la spiegazione estesa delle tappe è in `content/lezioni/M09.md`.
