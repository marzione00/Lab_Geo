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

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**33 slide · 10 figure · 9 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M09_R6.pdf) · [Codice R delle figure](../../materiali/R/M09_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M09_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Tempo e provenienza delle osservazioni.
- Pagina 7: Aggregazione, copertura e risoluzione.
- Pagina 10: Componenti, smoothing e riferimenti.
- Pagina 16: Ritardi e autocorrelazione.
- Pagina 19: Processi e stazionarietà.
- Pagina 24: Trend, differenze e trasformazioni.
- Pagina 29: Diagnosi con ADF e KPSS.
- Pagina 32: Laboratorio e riferimenti.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M09_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

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

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
