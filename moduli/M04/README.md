# M04 · Probabilità, variabilità e simulazione

Modelli del caso e propagazione dell’incertezza in R.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

9 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M04`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Eventi e frequenze relative** · `#laboratorio/m04-eventi` | Confrontare probabilità dichiarata e frequenza simulata. | [R](../../R/experiments/m04-eventi.R) |
| **Probabilità condizionata** · `#laboratorio/m04-condizionamento` | Distinguere probabilità marginale e probabilità entro un gruppo. | [R](../../R/experiments/m04-condizionamento.R) |
| **Distribuzione cumulativa e quantili** · `#laboratorio/m04-distribuzione` | Collegare densità, area e probabilità cumulativa. | [R](../../R/experiments/m04-distribuzione.R) |
| **Bernoulli e distribuzione binomiale** · `#laboratorio/m04-binomiale` | Collegare prove elementari e conteggio dei successi. | [R](../../R/experiments/m04-binomiale.R) |
| **Conteggi ed esposizione** · `#laboratorio/m04-poisson` | Distinguere tasso e numero atteso di eventi. | [R](../../R/experiments/m04-poisson.R) |
| **Standardizzazione e quantili normali** · `#laboratorio/m04-normale` | Collegare unità originali e unità standardizzate. | [R](../../R/experiments/m04-normale.R) |
| **Variabilità moltiplicativa** · `#laboratorio/m04-moltiplicazione` | Esaminare un prodotto di fattori positivi. | [R](../../R/experiments/m04-moltiplicazione.R) |
| **Precisione della simulazione Monte Carlo** · `#laboratorio/m04-monte-carlo` | Separare incertezza numerica e variabilità del fenomeno. | [R](../../R/experiments/m04-monte-carlo.R) |
| **Propagare incertezze correlate** · `#laboratorio/m04-propagazione` | Valutare l’incertezza di un rapporto fra misure positive. | [R](../../R/experiments/m04-propagazione.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**35 slide · 10 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M04_R6.pdf) · [Codice R delle figure](../../materiali/R/M04_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M04_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Esiti, eventi e probabilità.
- Pagina 6: Condizionamento e indipendenza.
- Pagina 9: Variabili casuali e distribuzioni.
- Pagina 12: Bernoulli e binomiale.
- Pagina 15: Poisson ed esposizione.
- Pagina 19: Normale, standardizzazione e quantili.
- Pagina 23: Variabili positive e meccanismi moltiplicativi.
- Pagina 26: Repliche e precisione Monte Carlo.
- Pagina 29: Propagazione dell’incertezza.
- Pagina 34: Laboratorio e riferimenti.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M04_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M04_N01 | Evento e probabilità: una regola dichiarata | [R](../../materiali/laboratori/M04/M04_N01.R) |
| M04_N02 | Eventi complementari e soglie | [R](../../materiali/laboratori/M04/M04_N02.R) |
| M04_N03 | Una tabella per la probabilità condizionata | [R](../../materiali/laboratori/M04/M04_N03.R) |
| M04_N04 | Indipendenza: non basta una somiglianza visiva | [R](../../materiali/laboratori/M04/M04_N04.R) |
| M04_N05 | La binomiale: numero di successi in n prove | [R](../../materiali/laboratori/M04/M04_N05.R) |
| M04_N06 | Calcolare probabilità di eventi composti | [R](../../materiali/laboratori/M04/M04_N06.R) |
| M04_N07 | Verificare una probabilità con simulazioni | [R](../../materiali/laboratori/M04/M04_N07.R) |
| M04_N08 | Poisson: conteggi con esposizione dichiarata | [R](../../materiali/laboratori/M04/M04_N08.R) |
| M04_N09 | Una miscela può violare il modello semplice | [R](../../materiali/laboratori/M04/M04_N09.R) |
| M04_N10 | Un modello continuo non assegna probabilità ai singoli punti | [R](../../materiali/laboratori/M04/M04_N10.R) |
| M04_N11 | Standardizzare e ritrovare le probabilità | [R](../../materiali/laboratori/M04/M04_N11.R) |
| M04_N12 | Dati positivi e asimmetria | [R](../../materiali/laboratori/M04/M04_N12.R) |
| M04_N13 | Disegnare l’esperimento di incertezza | [R](../../materiali/laboratori/M04/M04_N13.R) |
| M04_N14 | Propagare l’incertezza con molte estrazioni | [R](../../materiali/laboratori/M04/M04_N14.R) |
| M04_N15 | Leggere la distribuzione del risultato | [R](../../materiali/laboratori/M04/M04_N15.R) |
| M04_N16 | Controllo con un’approssimazione analitica | [R](../../materiali/laboratori/M04/M04_N16.R) |
| M04_N17 | Che cosa cambia se gli errori sono correlati? | [R](../../materiali/laboratori/M04/M04_N17.R) |
| M04_N18 | Errore casuale e bias non sono la stessa cosa | [R](../../materiali/laboratori/M04/M04_N18.R) |
| M04_N19 | Laboratorio applicativo — Probabilità normale | [R](../../materiali/laboratori/M04/M04_N19.R) |
| M04_N20 | Laboratorio applicativo — Migliorare uno strumento | [R](../../materiali/laboratori/M04/M04_N20.R) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
