# M05 · Campionamento, stima e incertezza

Disegni campionari, derivazioni e ricampionamento strutturato.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

9 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M05`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Campionare per misure o per stazioni** · `#laboratorio/m05-estimandi` | Confrontare bersagli definiti da pesi differenti. | [R](../../R/experiments/m05-estimandi.R) |
| **Precisione e bias di selezione** · `#laboratorio/m05-selezione` | Osservare l’effetto della selezione su campagne ripetute. | [R](../../R/experiments/m05-selezione.R) |
| **Distribuzione campionaria della media** · `#laboratorio/m05-distribuzioni` | Distinguere dati individuali e statistiche campionarie. | [R](../../R/experiments/m05-distribuzioni.R) |
| **Errore standard e dipendenza** · `#laboratorio/m05-dipendenza` | Quantificare il contributo delle covarianze alla precisione della media. | [R](../../R/experiments/m05-dipendenza.R) |
| **Copertura degli intervalli di confidenza** · `#laboratorio/m05-intervalli` | Osservare la copertura frequentista in campioni ripetuti. | [R](../../R/experiments/m05-intervalli.R) |
| **Ricampionare il campione osservato** · `#laboratorio/m05-bootstrap` | Costruire una distribuzione bootstrap e un intervallo percentile. | [R](../../R/experiments/m05-bootstrap.R) |
| **Ricampionamento per stazioni** · `#laboratorio/m05-ricampionamento` | Confrontare bootstrap delle misure e delle unità indipendenti. | [R](../../R/experiments/m05-ricampionamento.R) |
| **Bootstrap a blocchi di una serie dipendente** · `#laboratorio/m05-blocchi` | Confrontare ricampionamento individuale e ricampionamento di sequenze temporali. | [R](../../R/experiments/m05-blocchi.R) |
| **Stabilità numerica di un quantile bootstrap** · `#laboratorio/m05-precisione` | Valutare l’incertezza dovuta al numero finito di ricampionamenti. | [R](../../R/experiments/m05-precisione.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**105 slide · 28 figure · 24 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M05_R6.pdf) · [Codice R delle figure](../../materiali/R/M05_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M05_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Apertura.
- Pagina 4: Estimandi e disegni.
- Pagina 15: Selezione e distorsione.
- Pagina 22: Distribuzioni campionarie.
- Pagina 34: Errore standard.
- Pagina 44: Intervalli.
- Pagina 55: Bootstrap elementare.
- Pagina 69: Disegno del ricampionamento.
- Pagina 86: Precisione numerica.
- Pagina 93: Esercizi.
- Pagina 104: Riferimenti.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M05_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M05_N01 | Parametro, campione e statistica | [R](../../materiali/laboratori/M05/M05_N01.R) |
| M05_N02 | Media cumulativa e convergenza | [R](../../materiali/laboratori/M05/M05_N02.R) |
| M05_N03 | Distribuzione delle medie | [R](../../materiali/laboratori/M05/M05_N03.R) |
| M05_N04 | Standardizzazione e dipendenza | [R](../../materiali/laboratori/M05/M05_N04.R) |
| M05_N05 | Dispersione dei dati ed errore standard | [R](../../materiali/laboratori/M05/M05_N05.R) |
| M05_N06 | Intervallo di Student | [R](../../materiali/laboratori/M05/M05_N06.R) |
| M05_N07 | Copertura della procedura | [R](../../materiali/laboratori/M05/M05_N07.R) |
| M05_N08 | Precisione, selezione e popolazione finita | [R](../../materiali/laboratori/M05/M05_N08.R) |
| M05_N09 | Pesi, precisione richiesta e conclusione | [R](../../materiali/laboratori/M05/M05_N09.R) |
| M05_N10 | Distribuzione empirica e informazione | [R](../../materiali/laboratori/M05/M05_N10.R) |
| M05_N11 | Una replica osservata negli indici | [R](../../materiali/laboratori/M05/M05_N11.R) |
| M05_N12 | Bootstrap della media di un gruppo | [R](../../materiali/laboratori/M05/M05_N12.R) |
| M05_N13 | Pooled e quote casuali | [R](../../materiali/laboratori/M05/M05_N13.R) |
| M05_N14 | Bootstrap stratificato | [R](../../materiali/laboratori/M05/M05_N14.R) |
| M05_N15 | Contrasti indipendenti e coppie | [R](../../materiali/laboratori/M05/M05_N15.R) |
| M05_N16 | Provini e medie di stazione | [R](../../materiali/laboratori/M05/M05_N16.R) |
| M05_N17 | Contrasto fra affioramenti | [R](../../materiali/laboratori/M05/M05_N17.R) |
| M05_N18 | Precisione Monte Carlo e registrazione | [R](../../materiali/laboratori/M05/M05_N18.R) |
| M05_N19 | Reinserimento e bootstrap enumerato | [R](../../materiali/laboratori/M05/M05_N19.R) |
| M05_N20 | Mediana e confronto fra statistiche | [R](../../materiali/laboratori/M05/M05_N20.R) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
