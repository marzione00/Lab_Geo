# M14 · Estremi, pericolosità e rischio

Superamenti, tempi di ritorno e incertezza dei livelli rari.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

7 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M14`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Dalle osservazioni ai massimi annuali** · `#laboratorio/m14-massimi` | Esaminare la distribuzione dei massimi di blocchi indipendenti. | [R](../../R/experiments/m14-massimi.R) |
| **Tempo di ritorno e orizzonte temporale** · `#laboratorio/m14-ritorno` | Distinguere probabilità annuale, attesa e rischio cumulato. | [R](../../R/experiments/m14-ritorno.R) |
| **Adattamento di Gumbel ai massimi** · `#laboratorio/m14-gumbel` | Confrontare distribuzione empirica e modello stimato ai momenti. | [R](../../R/experiments/m14-gumbel.R) |
| **Livelli di ritorno e incertezza bootstrap** · `#laboratorio/m14-livelli-rari` | Esaminare l’incertezza di un livello raro condizionatamente al modello. | [R](../../R/experiments/m14-livelli-rari.R) |
| **Sensibilità alla forma della coda GEV** · `#laboratorio/m14-gev` | Confrontare livelli rari sotto forme di coda differenti. | [R](../../R/experiments/m14-gev.R) |
| **Superamenti e separazione degli episodi** · `#laboratorio/m14-episodi` | Distinguere giorni sopra soglia ed eventi temporali. | [R](../../R/experiments/m14-episodi.R) |
| **Pericolosità e conseguenze** · `#laboratorio/m14-conseguenze` | Calcolare la perdita attesa per classi di evento mutuamente esclusive. | [R](../../R/experiments/m14-conseguenze.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**31 slide · 12 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M14_R6.pdf) · [Codice R delle figure](../../materiali/R/M14_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M14_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Massimi annuali e probabilità empiriche.
- Pagina 8: Ritorno, attesa e orizzonte temporale.
- Pagina 13: Modello Gumbel e verifica dell’adattamento.
- Pagina 18: Livelli rari e incertezza della stima.
- Pagina 24: Forma della coda e sensibilità GEV.
- Pagina 26: Superamenti giornalieri ed episodi.
- Pagina 29: Pericolosità, conseguenze e comunicazione.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M14_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M14_N01 | Audit dei massimi annuali | [R](../../materiali/laboratori/M14/M14_N01.R) |
| M14_N02 | Posizioni empiriche di superamento | [R](../../materiali/laboratori/M14/M14_N02.R) |
| M14_N03 | CDF e probabilità di superamento | [R](../../materiali/laboratori/M14/M14_N03.R) |
| M14_N04 | Tempo di ritorno non significa appuntamento | [R](../../materiali/laboratori/M14/M14_N04.R) |
| M14_N05 | Probabilità durante una vita utile | [R](../../materiali/laboratori/M14/M14_N05.R) |
| M14_N06 | Simulare i tempi di attesa geometrici | [R](../../materiali/laboratori/M14/M14_N06.R) |
| M14_N07 | Quantili empirici e supporto osservato | [R](../../materiali/laboratori/M14/M14_N07.R) |
| M14_N08 | Gumbel: stima dei parametri con i momenti | [R](../../materiali/laboratori/M14/M14_N08.R) |
| M14_N09 | CDF e quantile Gumbel: controllo inverso | [R](../../materiali/laboratori/M14/M14_N09.R) |
| M14_N10 | QQ plot: dove il modello descrive peggio? | [R](../../materiali/laboratori/M14/M14_N10.R) |
| M14_N11 | Livelli di ritorno e distanza dall’osservato | [R](../../materiali/laboratori/M14/M14_N11.R) |
| M14_N12 | Bootstrap dei massimi annuali | [R](../../materiali/laboratori/M14/M14_N12.R) |
| M14_N13 | Lunghezza del record e stabilità della stima | [R](../../materiali/laboratori/M14/M14_N13.R) |
| M14_N14 | Quanto conta il massimo isolato? | [R](../../materiali/laboratori/M14/M14_N14.R) |
| M14_N15 | Due periodi: descrivere prima di attribuire | [R](../../materiali/laboratori/M14/M14_N15.R) |
| M14_N16 | Forma della GEV: una sensibilità, non un fit | [R](../../materiali/laboratori/M14/M14_N16.R) |
| M14_N17 | Superamenti giornalieri e numero di episodi | [R](../../materiali/laboratori/M14/M14_N17.R) |
| M14_N18 | Declustering di sequenze consecutive | [R](../../materiali/laboratori/M14/M14_N18.R) |
| M14_N19 | Pericolosità ed esposizione: perdita attesa di scenario | [R](../../materiali/laboratori/M14/M14_N19.R) |
| M14_N20 | Relazione finale: livello, metodo e condizioni | [R](../../materiali/laboratori/M14/M14_N20.R) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
